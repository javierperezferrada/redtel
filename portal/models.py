#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Mensaje(models.Model):
	id=models.AutoField(primary_key=True)
	msg = models.CharField(max_length=1024)

class Usuario(models.Model):
	id=models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=45)
	rut = models.CharField(max_length=45)
	zonal = models.CharField(max_length=45)
	afp =models.CharField(max_length=45)
	salud = models.CharField(max_length=45)
	ccosto = models.CharField(max_length=45)
	cargo = models.CharField(max_length=45)
	fecha_ingreso = models.CharField(max_length=45)
	direccion = models.CharField(max_length=100)
	comuna = models.CharField(max_length=45)
	celular = models.CharField(max_length=45)
	telefono = models.CharField(max_length=45)
	f_nac = models.CharField(max_length=45)
	correo = models.CharField(max_length=45)
	est_civil = models.CharField(max_length=45)
	nacionalidad = models.CharField(max_length=45)
	licencia = models.CharField(max_length=45)
	cargas_fam = models.CharField(max_length=45)
	n_hijos = models.CharField(max_length=45)
	f_contrato = models.CharField(max_length=45)
	vencimiento = models.CharField(max_length=45)
	tipo_pago = models.CharField(max_length=45)
	n_cuenta = models.CharField(max_length=45)

class Us(models.Model):
    id = models.IntegerField(primary_key=True)  
    username = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    rut = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'usuario'


class Liquidacion(models.Model):
	id=models.AutoField(primary_key=True)
	Usuario_rut = models.CharField(max_length=15)
	mes = models.CharField(max_length=20)

	zonal = models.CharField(max_length=20)
	c_costo = models.CharField(max_length=40)
	dias = models.IntegerField()
	sueldo = models.IntegerField()
	h_extras = models.IntegerField()
	bonos_impon = models.IntegerField()
	gratificacion = models.IntegerField()
	total_impon = models.IntegerField()
	movilizacion = models.IntegerField()
	colacion = models.IntegerField()
	otros_no_impon = models.IntegerField()
	asig_fam = models.IntegerField()
	total_no_impon = models.IntegerField()
	total_haberes = models.IntegerField()
	afp = models.IntegerField()
	seg_cesantia = models.IntegerField()
	sis = models.IntegerField()
	ahorro_afp = models.IntegerField()	
	salud = models.IntegerField()
	mutual = models.IntegerField()
	impto_unico = models.IntegerField()
	prestamo_ccaf = models.IntegerField()
	prestamos = models.IntegerField()
	anticipos = models.IntegerField()
	otros_dsctos = models.IntegerField()
	total_dsctos = models.IntegerField()
	liquido_pago = models.IntegerField()


