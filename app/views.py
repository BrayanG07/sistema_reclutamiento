from unittest import result
from django.shortcuts import render, redirect
from .models import Job_Position, Skills, Vacant

# Create your views here.

def inicio(request):
    return render(request, 'pages/index.html')

def vacantes(request):

    list_job_position = Job_Position.objects.all();
    
    if request.POST:
        if request.POST['txtJobPosition'] == '0':
            print("SELECCIONAR AREA DE TRABAJO")
            return render(request, 'pages/vacantes.html', {'list_job_position': list_job_position})

        resultado = evaluarFiltros(request)
        
        vacantes = Vacant.objects.raw(resultado[1], resultado[0])
        skills = Vacant.objects.raw(resultado[2], resultado[0])

        lists = {
            'list_job_position': list_job_position, 
            'list_vacant': vacantes,
            'list_skills': skills,
        }

        return render(request, 'pages/vacantes.html', lists)
    else:
        sql = "SELECT v.id, v.name_complete, TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) as experience_start_date, v.city, v.email, v.country, v.modality, j.name FROM app_vacant v INNER JOIN app_job_position j ON v.job_position_id = j.id WHERE v.job_position_id BETWEEN 1 AND 3 AND v.country = 'Honduras'"
        vacantes = Vacant.objects.raw(sql)

        query = "SELECT id, name, vacant_id FROM app_skills WHERE vacant_id IN (SELECT id FROM app_vacant WHERE job_position_id BETWEEN 1 AND 3 AND country = 'Honduras')"
        skills = Skills.objects.raw(query)

        lists = {
            'list_job_position': list_job_position, 
            'list_vacant': vacantes,
            'list_skills': skills,
        }

        return render(request, 'pages/vacantes.html', lists)

def evaluarFiltros(request):
    if request.POST:
        arregloSkills = []
        resultado = []
        filtros = []
        city = ""
        country = ""
        modality = ""
        sql = "SELECT v.id, v.name_complete, TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) as experience_start_date, v.city, v.email, v.country, v.modality, j.name FROM app_vacant v INNER JOIN app_job_position j ON v.job_position_id = j.id WHERE v.job_position_id = %s "
        query = "SELECT id, name, vacant_id FROM app_skills WHERE vacant_id IN (SELECT id FROM app_vacant WHERE job_position_id = %s "

        job_position = request.POST['txtJobPosition']
        years_experience = request.POST['txtYearExperience']
        cantidad_skills = int(request.POST['txtCantidadSkills'])

        if years_experience == "":
            years_experience = 0
        
        if request.POST['txtCountry'] != "":
            country = request.POST['txtCountry']    
        
        if request.POST['txtUbication'] != "":
            city = request.POST['txtUbication']
        
        if request.POST['txtModality'] != "":
            modality = request.POST['txtModality']
  
        
        for i in range(0, (cantidad_skills + 1), 1):
            skill = request.POST['txtSkill'+str(i)]
            if skill != '':
                arregloSkills.append(skill)
        
        if len(arregloSkills) == 0:
            
            if  country != "" and city != "" and modality != "": 

                print("ENTRANDO FILTRO 1")

                filtros = [int(job_position), country, "%"+city+"%", modality, int(years_experience) ]
                sql = sql+" AND v.country = %s AND v.city LIKE %s AND v.modality = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND country = %s AND city LIKE %s AND modality = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"

            if  country == "" and city != "" and modality != "":

                print("ENTRANDO FILTRO 2")

                filtros = [int(job_position), "%"+city+"%", modality, int(years_experience) ]
                sql = sql+" AND v.city LIKE %s AND v.modality = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND city LIKE %s AND modality = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"                                

            if country == "" and city == "" and modality != "":
                print("ENTRANDO FILTRO 3")

                filtros = [int(job_position), modality, int(years_experience) ]
                sql = sql+" AND v.modality = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND modality = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"   

            if country == "" and city == "" and modality == "":
                print("ENTRANDO FILTRO 4")

                filtros = [int(job_position), int(years_experience) ]
                sql = sql+" AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"       

            if country != "" and city == "" and modality == "":
                print("ENTRANDO FILTRO 5")

                filtros = [int(job_position), country, int(years_experience) ]
                sql = sql+" AND v.country = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND country = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"
            
            if country != "" and city == "" and modality != "":
                print("ENTRANDO FILTRO 6")

                filtros = [int(job_position), country, modality, int(years_experience) ]
                sql = sql+" AND v.country = %s AND v.modality = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND country = %s AND modality = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"
            
            if country != "" and city != "" and modality == "":
                print("ENTRANDO FILTRO 7")

                filtros = [int(job_position), country, "%"+city+"%", int(years_experience) ]
                sql = sql+" AND v.country = %s AND v.city LIKE %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND country = %s AND city LIKE %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"
            
            if country == "" and city != "" and modality == "":
                print("ENTRANDO FILTRO 8")

                filtros = [int(job_position),"%"+city+"%", int(years_experience) ]
                sql = sql+" AND v.city LIKE %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND city LIKE %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"

            resultado.append(filtros)
            resultado.append(sql)
            resultado.append(query)

            return resultado
        else:
            print('OTRO TIPO DE CONSULTA')
        
        print(arregloSkills)        
        print(resultado)        
        print(job_position)        
        print(country)        
        print(city)        
        print(years_experience)        
        print(modality) 
        return resultado


