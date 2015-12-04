# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse


import os
#Librerias reportlab a usar:
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO 
from reportlab.pdfgen import canvas
from .models import Usuario, Us
from .models import Liquidacion
from django.contrib import messages
import csv
from .forms import UploadFileForm


def index(request):
    return render_to_response('index.html')

#@login_required()
def home(request):
   return render_to_response('home.html', {'user': request.user}, context_instance=RequestContext(request))



@login_required()
def mis_datos(request):
	usuario = get_object_or_404(Usuario, rut=request.user.first_name)
	return render_to_response('mis_datos.html', {'usuario': usuario}, context_instance=RequestContext(request))

#@login_required()
#def obtener_certificado(request):
#    usuario = get_object_or_404(Usuario, id=request.user.id)
#    return render_to_response('obtener_certificado.html', {'usuario': usuario}, context_instance=RequestContext(request))

@login_required()
def mis_liquidaciones(request):
    liquidaciones = Liquidacion.objects.filter(Usuario_rut=request.user.first_name)
    return render_to_response('mis_liquidaciones.html', {'liquidaciones': liquidaciones}, context_instance=RequestContext(request))

@login_required()
def liq_detalle(request):
    usuario = get_object_or_404(Usuario, id=request.user.id)
    liquidaciones = Liquidacion.objects.filter(Usuario_rut=usuario.rut)
    return render_to_response('mis_liquidaciones.html', {'liquidaciones': liquidaciones}, context_instance=RequestContext(request))


@login_required()
def obtener_certificado(request):
    try: 
        usuario = Usuario.objects.get(rut=request.user.first_name)
    except ValueError: 
        raise Http404() 
    respuesta = HttpResponse(content_type = 'application/pdf')
    respuesta['Content-Disposition'] = 'filename = "certificado.pdf"'


    Q = SimpleDocTemplate(respuesta,rightMargin=72,leftMargin=72,topMargin=72,BottomMargin=18)
    Story = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Header',alignment=1,spaceBefore=85,fontSize=20,leading=22))
    styles.add(ParagraphStyle(name='Estilo01',alignment = 2))
    styles.add(ParagraphStyle(name='Estilo02',alignment = 0,firstLineIndent=100,spaceBefore=50,fontSize=18,leading=20))
    styles.add(ParagraphStyle(name='Pie',spaceBefore=100,alignment=2))

    ptext = 'Servicios e Ingenieria Ltda.'
    ptext2 = 'Valdivia, Chile (Agregar fecha)'
    pa = Paragraph(ptext,styles['Estilo01'])
    pa2 = Paragraph(ptext2,styles['Estilo01'])
    #im = Image("media/logo.gif")
    #im.halign="LEFT"

    #data = [[im,pa],['',pa2]]

    #TTemp = Table(data,colWidths=90)

    #Story.append(TTemp)

    HText = "CERTIFICADO DE ANTIGUEDAD LABORAL"

    Header = Paragraph(HText,styles['Header'])

    Story.append(Header)

    ptext = '<b>JULIO GUIDILFREDO ZARECHT ORTEGA</b>, rut 7.385,055-K representante legal de <b>Servicios e Ingenieria Limitada</b>,\
     Rut: 77.869.650-9 por medio de la presente, certifica que don:'+usuario.nombre+', RUT:'+usuario.rut+' , es trabajador de esta empresa, \
     se desempena como Encargado RRHH, con contrato vigente desde el <b>'+usuario.fecha_ingreso+'</b> y es de caracter <b>Indefinido</b>, y registra\
     domicilio segun contrato en <b>'+usuario.direccion+'</b>, de Valdivia'

    TTemp = Paragraph(ptext,styles['Estilo02'])

    Story.append(TTemp)

    ptext = 'Se emite el presente certificado a peticion del interesado para ser presentadoen <b>AFP</b>'

    TTemp = Paragraph(ptext,styles['Estilo02'])

    Story.append(TTemp)

    ptext = "JULIO GUIDILFREDO ZARECHT ORTEGA <br/> Representante Legal"

    TTemp = Paragraph(ptext,styles['Pie'])

    Story.append(TTemp)

    Q.build(Story)

    respuesta.close()

    return respuesta

@login_required()
def imprimir_liquidacion(request,pk):   
    try: 
        liquidacion = Liquidacion.objects.get(id=pk) 
        usuario = Usuario.objects.get(rut=request.user.first_name)
    except ValueError: # Si no existe llamamos a "pagina no encontrada". 
        raise Http404()  
    response = HttpResponse(content_type='application/pdf') 
    response['Content-Disposition'] = "attachment; filename="+str(liquidacion.mes)+".pdf"
    Q = SimpleDocTemplate(response,rightMargin=30,leftMargin=30,topMargin=20,BottomMargin=5)
    Story = []
    styles = getSampleStyleSheet()
    t = Table([
        ['Empleador','SERVICIOS E INGENIERIA LTDA','','','','',''],
        ['R.U.T.','77.869.650-9','','','','',''],
        ['Dirección','AVDA. PICARTE 3644, INTERIOR, VALDIVIA','','','','',''],
        ['','','','','','',''],
        ['','','LIQUIDACION DE SUELDO MES '+liquidacion.mes.upper(),'','','',''],
        ['','','','','','',''],
        ['NOMBRE',usuario.nombre,'','','','RUT',usuario.rut],
        ['C.COSTO',usuario.ccosto,'','','','AREA',usuario.zonal],
        ['CARGO',usuario.cargo,'','','','FECHA ING',usuario.fecha_ingreso],
        ['AFP',usuario.afp,'','','','SALUD',usuario.salud],
        ['DIAS TRABAJADOS',liquidacion.dias,'LICENCIA','','AUSENTE','',''],
        ['','','','','','',''],
        ['','','','HABERES','','',''],
        ['','','','','','',''],
        ['SUELDO DEL MES','','','','','',liquidacion.sueldo],
        ['GRATIFICACION','','','','','',liquidacion.gratificacion],
        ['COMISION PRODUCCION','','','','','',liquidacion.bonos_impon],
        ['HORAS EXTRAS','','','','','',liquidacion.h_extras],
        ['TOTAL HABERES IMPONIBLES','','','','','',liquidacion.total_impon],
        ['ASIGNACION VIATICOS','','','','','',liquidacion.colacion],
        ['MOVILIZACION COMBUSTIBLE','','','','','',liquidacion.movilizacion],
        ['TOTAL NO IMPONIBLE','','','','','',liquidacion.total_no_impon],
        ['TOTAL HABERES','','','','','',liquidacion.total_haberes],
        ['','','','','','',''],
        ['','','','DESCUENTOS','','',''],
        ['','','','','','',''],
        ['AFP','','','','','',liquidacion.afp],
        ['SALUD','','','','','',liquidacion.salud],
        ['SEGURO CESANTIA','','','','','',liquidacion.seg_cesantia],
        ['TOTAL DESCUENTOS LEGALES','','','','','',''],
        ['ANTICIPOS','','','','','',''],
        ['TOTAL OTROS DESCUENTOS','','','','','',liquidacion.otros_dsctos],
        ['TOTAL DESCUENTOS','','','','','',liquidacion.total_dsctos],
        ['','','','','','',''],
        ['','','','','','',''],
        ['LIQUIDO A PAGAR','','','','','',liquidacion.liquido_pago],
        ['','','','','','',''],
        ['','','','','','',''],
        ['-------------','','','','','','--------------'],
        ['Firma Representante Legal','','','','','Recibí Conforme(Firma)',''],
        ['JULIO ZARECHT ORTEGA','','','','',usuario.nombre,''],
        ['R.U.T.:7.385.055-K','','','','','R.U.T.:'+usuario.rut,''],
    ], colWidths=80, rowHeights=10)
    Story.append(t)
    Q.build(Story)
    response.close()
    return response

@login_required()
def imprimir_ultima(request):  
    try: 
        usuario = get_object_or_404(Usuario, id=request.user.id)
        qs = Liquidacion.objects.filter(Usuario_rut=usuario.rut)
        qs = qs.latest("mes")
    except ValueError: 
        raise Http404() 
    response = HttpResponse(content_type='application/pdf') 
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    buffer = BytesIO() 
    p = canvas.Canvas(buffer) 
    p.drawString(100, 800, "Rut trabajador")
    p.drawString(300, 800, str(qs.Usuario_rut))
    p.drawString(100, 790, "mes")
    p.drawString(300, 790, str(qs.mes))
    p.drawString(100, 780, "Sueldo")
    p.drawString(300, 780, str(qs.sueldo))
    p.drawString(100, 770, "Gratificacion legal")
    p.drawString(300, 770, str(qs.gratificacion))
    p.drawString(100, 760, "AFP")
    p.drawString(300, 760, str(qs.afp))
    p.drawString(100, 750, "Anticipo")
    p.drawString(300, 750, str(qs.anticipo))
    p.showPage() 
    p.save() 
    pdf = buffer.getvalue() 
    buffer.close() 
    response.write(pdf) 
    return response

@login_required()
def copias_liquidaciones(request):
    usuario = get_object_or_404(Usuario, id=request.user.id)
    return render_to_response('copias_liquidaciones.html', {'usuario': usuario}, context_instance=RequestContext(request))

@permission_required('portal.puede_cargar', login_url="/ingresar") 
def cargar_usuarios(request):	
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            reader = csv.reader(request.FILES['docfile'])
            index = 0
            for index,row in enumerate(reader):
                if index<7:
                    print 'cabecera'
                else: 
                    usuarios = Usuario()
                    usuarios.nombre = row[1]
                    usuarios.rut = row[4]
                    usuarios.zonal = row[2]
                    usuarios.afp =row[18]
                    usuarios.salud = row[19]
                    usuarios.ccosto = row[3]
                    usuarios.cargo = row[29]
                    usuarios.fecha_ingreso = row[16]
                    usuarios.direccion = row[5]
                    usuarios.comuna = row[6]
                    usuarios.celular = row[7]
                    usuarios.telefono = row[8]
                    usuarios.f_nac = row[9]
                    usuarios.correo = row[10]
                    usuarios.est_civil = row[11]
                    usuarios.nacionalidad = row[12]
                    usuarios.licencia = row[13]
                    usuarios.cargas_fam = row[14]
                    usuarios.n_hijos = row[15]
                    usuarios.f_contrato = row[17]
                    usuarios.vencimiento = row[20]
                    usuarios.tipo_pago = row[21]
                    usuarios.n_cuenta = row[22]
                    usuarios.save()
            return HttpResponseRedirect('/home')
    else:
        form = UploadFileForm()
    return render_to_response('cargar_usuarios.html', {'form': form}, context_instance=RequestContext(request))

@permission_required('portal.puede_cargar', login_url="/ingresar")  
def cargar_liquidaciones(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            reader = csv.reader(request.FILES['docfile'])
            index = 0
            for index,row in enumerate(reader):
                if index<7:
                    if index == 1:
                        s=row[0]
                        mes_data = s[16:]

                else: 
                    liquidaciones = Liquidacion()
                    liquidaciones.Usuario_rut = row[1]
                    liquidaciones.mes = mes_data
                    liquidaciones.zonal = row[2]
                    liquidaciones.c_costo = row[3]
                    liquidaciones.dias = row[4]
                    liquidaciones.sueldo = row[5]
                    liquidaciones.h_extras = row[6]
                    liquidaciones.bonos_impon = row[7]
                    liquidaciones.gratificacion = row[8]
                    liquidaciones.total_impon = row[9]
                    liquidaciones.movilizacion = row[10]
                    liquidaciones.colacion = row[11]
                    liquidaciones.otros_no_impon = row[12]
                    liquidaciones.asig_fam = row[13]
                    liquidaciones.total_no_impon = row[14]
                    liquidaciones.total_haberes = row[15]
                    liquidaciones.afp = row[16]
                    liquidaciones.seg_cesantia = row[17]
                    liquidaciones.anticipo_combustible = row[18]
                    liquidaciones.sis = row[19]
                    liquidaciones.ahorro_afp = row[20]
                    liquidaciones.salud = row[21]
                    liquidaciones.mutual = row[22]
                    liquidaciones.impto_unico = row[23]
                    liquidaciones.prestamo_ccaf = row[24]
                    liquidaciones.prestamos = row[25]
                    liquidaciones.anticipos = row[26]
                    liquidaciones.otros_dsctos = row[27]
                    liquidaciones.total_dsctos = row[28]
                    liquidaciones.liquido_pago = row[29]
                    liquidaciones.save()
            return HttpResponseRedirect('/home')
    else:
        form = UploadFileForm()
    return render_to_response('cargar_liquidaciones.html', {'form': form}, context_instance=RequestContext(request))


@login_required()
def us(request):
    with open('us_rut.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            user = Us()
            user.username = row[0]
            user.password = row[2]
            user.rut = row[1]
            user.save()
        return HttpResponseRedirect('/home')

