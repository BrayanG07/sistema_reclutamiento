from django.shortcuts import render, redirect
from .models import Job_Position, Skills, Vacant

# Create your views here.

def inicio(request):
    return render(request, 'pages/index.html')

def vacantes(request):
    list_job_position = Job_Position.objects.all();
    filters = [7, '', '', '']

    sql = "SELECT v.id, v.name_complete, TIMESTAMPDIFF(YEAR, v.experience_start_date, CURRENT_DATE()) as experience_start_date, v.city, v.email, v.country, v.modality, j.name 	FROM app_vacant v INNER JOIN app_job_position j ON v.job_position_id = j.id WHERE job_position_id = %s OR UPPER(country) = %s OR UPPER(city) = %s OR UPPER(modality) = %s"
    vacantes = Vacant.objects.raw(sql, filters)

    query = "SELECT id, name, vacant_id FROM app_skills WHERE vacant_id IN (SELECT id FROM app_vacant WHERE job_position_id =  %s OR UPPER(country) = %s OR UPPER(city) = %s OR UPPER(modality) = %s '')"
    skills = Skills.objects.raw(query, filters)

    lists = {
        'list_job_position': list_job_position, 
        'list_vacant': vacantes,
        'list_skills': skills,
    }

    return render(request, 'pages/vacantes.html', lists)
    #return render(request, 'pages/vacantes.html', {'list_job_position': list_job_position})