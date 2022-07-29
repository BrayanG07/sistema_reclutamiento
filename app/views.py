from unittest import result
from django.shortcuts import render, redirect
from .models import Job_Position, Skills, Vacant

# Create your views here.

def inicio(request):
    return render(request, 'pages/index.html')

def vacantes(request):

    list_job_position = Job_Position.objects.all();
    error = ""
    
    if request.POST:

        if request.POST['txtJobPosition'] == '0':
            error = "Debes seleccionar el area de trabajo para poder filtrar"
            return render(request, 'pages/vacantes.html', {'list_job_position': list_job_position, 'error': error})

        resultado = evaluarFiltros(request)

        vacantes = Vacant.objects.raw(resultado[1], resultado[0])
        skills = Vacant.objects.raw(resultado[2], resultado[0])

        # valores.append(job_position)
        # valores.append(years_experience)
        # valores.append(country)
        # valores.append(city)
        # valores.append(modality)

        print(resultado[3][0])

        lists = {
            'list_job_position': list_job_position, 
            'list_vacant': vacantes,
            'error': error,
            'job': int(resultado[3][0]),
            'years': resultado[3][1],
            'country': resultado[3][2],
            'city': resultado[3][3],
            'modality': resultado[3][4],
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
            'error': error
        }

        return render(request, 'pages/vacantes.html', lists)

def evaluarFiltros(request):
    if request.POST:
        listSkills = ""
        resultado = []
        filtros = []
        valores = []
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

        valores.append(job_position)
        valores.append(years_experience)
        valores.append(country)
        valores.append(city)
        valores.append(modality)

        index = (cantidad_skills + 1)
        for i in range(0, index , 1):
            skill = request.POST['txtSkill'+str(i)]
            if skill != '':
                if i == (index - 1):
                    listSkills = listSkills + "'" + skill.upper() + "'"
                else:
                    listSkills = listSkills + "'" + skill.upper() + "' , "
        
        if request.POST['txtSkill0'] == '':

            if  country != "" and city != "" and modality != "": 

                filtros = [int(job_position), country, "%"+city+"%", modality, int(years_experience) ]
                sql = sql+" AND v.country = %s AND v.city LIKE %s AND v.modality = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND country = %s AND city LIKE %s AND modality = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"

            if  country == "" and city != "" and modality != "":

                filtros = [int(job_position), "%"+city+"%", modality, int(years_experience) ]
                sql = sql+" AND v.city LIKE %s AND v.modality = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND city LIKE %s AND modality = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"                                

            if country == "" and city == "" and modality != "":

                filtros = [int(job_position), modality, int(years_experience) ]
                sql = sql+" AND v.modality = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND modality = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"   

            if country == "" and city == "" and modality == "":

                filtros = [int(job_position), int(years_experience) ]
                sql = sql+" AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"       

            if country != "" and city == "" and modality == "":

                filtros = [int(job_position), country, int(years_experience) ]
                sql = sql+" AND v.country = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND country = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"
            
            if country != "" and city == "" and modality != "":

                filtros = [int(job_position), country, modality, int(years_experience) ]
                sql = sql+" AND v.country = %s AND v.modality = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND country = %s AND modality = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"
            
            if country != "" and city != "" and modality == "":

                filtros = [int(job_position), country, "%"+city+"%", int(years_experience) ]
                sql = sql+" AND v.country = %s AND v.city LIKE %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND country = %s AND city LIKE %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"
            
            if country == "" and city != "" and modality == "":

                filtros = [int(job_position),"%"+city+"%", int(years_experience) ]
                sql = sql+" AND v.city LIKE %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s"
                query = query+" AND city LIKE %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s)"

            resultado.append(filtros)
            resultado.append(sql)
            resultado.append(query)
            resultado.append(valores)

            return resultado
        else:

            sql_find_skills = "SELECT v.id, v.name_complete, TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) as experience_start_date, v.city, v.email, v.country, v.modality, j.name FROM app_vacant v INNER JOIN app_job_position j ON v.job_position_id = j.id WHERE v.job_position_id = %s AND TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) >= %s "
            query_find_skills = "SELECT id, name, vacant_id FROM app_skills WHERE vacant_id IN (SELECT id FROM app_vacant WHERE job_position_id = %s AND TIMESTAMPDIFF(YEAR, experience_start_date, CURRENT_DATE()) >= %s  "
            skillFormated = "("+listSkills+")"

            if country == '' and city == '' and modality == '': # LISTOOOOO
                filtros = [int(job_position), int(years_experience)]
                
                sql_find_skills = sql_find_skills+" AND v.id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" )"
                query_find_skills = query_find_skills+" AND id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" ))"

            if  country != "" and city != "" and modality != "": # LISTOOOOO


                filtros = [int(job_position), int(years_experience), country, "%"+city+"%", modality]

                sql_find_skills = sql_find_skills+" AND v.id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" AND v.country = %s AND v.city LIKE %s AND v.modality = %s)"
                query_find_skills = query_find_skills+" AND country = %s AND city LIKE %s AND modality = %s AND id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" ))"

            if  country == "" and city != "" and modality != "": # LISTOOOOO


                filtros = [int(job_position), int(years_experience), "%"+city+"%", modality]

                sql_find_skills = sql_find_skills+" AND v.id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" AND v.city LIKE %s AND v.modality = %s)"
                query_find_skills = query_find_skills+" AND city LIKE %s AND modality = %s AND id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" ))"

            if country == "" and city == "" and modality != "": # LISTOOOOO

                filtros = [int(job_position), int(years_experience), modality]

                sql_find_skills = sql_find_skills+" AND v.id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" AND v.modality = %s)"
                query_find_skills = query_find_skills+" AND modality = %s AND id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" ))"   

            if country != "" and city == "" and modality == "": # LISTOOOOO

                filtros = [int(job_position), int(years_experience), country]

                sql_find_skills = sql_find_skills+" AND v.id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" AND v.country = %s)"
                query_find_skills = query_find_skills+" AND country = %s AND id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" ))"
            
            if country != "" and city == "" and modality != "": # LISTOOOOO

                filtros = [int(job_position), int(years_experience), country, modality]

                sql_find_skills = sql_find_skills+" AND v.id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" AND v.country = %s AND v.modality = %s)"
                query_find_skills = query_find_skills+" AND country = %s AND modality = %s AND id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" ))"
            
            if country != "" and city != "" and modality == "": # LISTOOOOO

                filtros = [int(job_position), int(years_experience), country, "%"+city+"%"]

                sql_find_skills = sql_find_skills+" AND v.id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" AND v.country = %s AND v.city LIKE %s)"
                query_find_skills = query_find_skills+" AND country = %s AND city LIKE %s AND id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" ))"
            
            if country == "" and city != "" and modality == "": # LISTOOOOO

                filtros = [int(job_position), int(years_experience), "%"+city+"%"]

                sql_find_skills = sql_find_skills+" AND v.id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" AND v.city LIKE %s )"
                query_find_skills = query_find_skills+" AND city LIKE %s AND id IN (SELECT DISTINCT vacant_id FROM app_skills WHERE UPPER(name) IN "+ skillFormated +" ))"


            resultado.append(filtros)
            resultado.append(sql_find_skills)
            resultado.append(query_find_skills) 
            resultado.append(valores) 
        
        return resultado


