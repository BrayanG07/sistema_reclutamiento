from django.db import models

# Create your models here.
class Job_Position(models.Model):
  name = models.CharField(max_length=100, verbose_name='Nombre')
  description = models.TextField(verbose_name='Descripcion', null=True)
  status = models.CharField(max_length=20, verbose_name='Estado')

  def __str__(self):
        return str(self.name)


class Vacant(models.Model):
    job_position = models.ForeignKey(
          Job_Position, 
          on_delete=models.CASCADE
    )        
  
    name_complete = models.CharField(max_length=200, verbose_name='Nombre Completo')
    experience_start_date = models.CharField(max_length=20, verbose_name='Fecha Inicio Experiencia')
    city = models.CharField(max_length=150, verbose_name='Ciudad')
    email = models.EmailField(max_length=250, verbose_name='Correo Electronico')
    dni = models.CharField(max_length=30, verbose_name='Identidad')
    status = models.CharField(max_length=25, verbose_name='Estado')
    country = models.CharField(max_length=50, verbose_name='Pais')
    modality = models.CharField(max_length=50, verbose_name='Modalidad')
  
    def __str__(self):
            return str(self.name_complete)

class Skills(models.Model):
    vacant = models.ForeignKey(
          Vacant, 
          on_delete=models.CASCADE
    )        
  
    name = models.CharField(max_length=100, verbose_name='Nombre')
  
    def __str__(self):
            return str(self.name)