from django.urls import path
from .views import view_fabricante, view_unidad, view_usuario, view_proveedor, view_estado, view_ubicacion, view_reactivo, view_orden, view_detalle_orden, view_reactivo_base, view_lugar, view_fase, view_codigo, view_cantidad,view_consecutivo, view_consumo

urlpatterns = [
    # urls para estado
    path('estado/<int:pk>/', view_estado.estado, name='estado'),
    path('estado/crear/', view_estado.crear_estado, name='crear_estado'),
    path('estado/listar/', view_estado.listar_estado, name='listar_estado'),
    # urls para usuario
    path('usuario/<int:pk>/', view_usuario.usuario, name='usuario'),
    path('usuario/crear/', view_usuario.crear_usuario, name='crear_usuario'),
    path('usuario/listar/', view_usuario.listar_usuario, name='listar_usuario'),
    # urls para fabricante
    path('fabricante/<int:pk>/', view_fabricante.fabricante, name='fabricante'),
    path('fabricante/crear/', view_fabricante.crear_fabricante,
         name='crear_fabricante'),
    path('fabricante/listar/', view_fabricante.listar_fabricante,
         name='listar_fabricante'),
    # urls para proveedor
    path('proveedor/<int:pk>/', view_proveedor.proveedor, name='proveedor'),
    path('proveedor/crear/', view_proveedor.crear_proveedor, name='crear_proveedor'),
    path('proveedor/listar/', view_proveedor.listar_proveedor,
         name='listar_proveedor'),
    # urls para ubicacion
    path('ubicacion/<int:pk>/', view_ubicacion.ubicacion, name='ubicacion'),
    path('ubicacion/crear/', view_ubicacion.crear_ubicacion, name='crear_ubicacion'),
    path('ubicacion/listar/', view_ubicacion.listar_ubicacion,
         name='listar_ubicacion'),
    # urls para reactivo
    path('reactivo/<int:pk>/', view_reactivo.reactivo, name='reactivo'),
    path('reactivo/crear/', view_reactivo.crear_reactivo, name='crear_reactivo'),
    path('reactivo/listar/', view_reactivo.listar_reactivo, name='listar_reactivo'),
    # urls para orden
    path('orden/<int:pk>/', view_orden.orden, name='orden'),
    path('orden/crear/', view_orden.crear_orden, name='crear_orden'),
    path('orden/listar/', view_orden.listar_orden, name='listar_orden'),
    # urls para detalle_orden
    path('detalle/<int:pk>/', view_detalle_orden.detalle, name='detalle'),
    path('detalle/crear/', view_detalle_orden.crear_detalle, name='crear_detalle'),
    path('detalle/listar/', view_detalle_orden.listar_detalle, name='listar_detalle'),
    # urls para unidad
    path('unidad/<int:pk>/', view_unidad.unidad, name='unidad'),
    path('unidad/crear/', view_unidad.crear_unidad, name='crear_unidad'),
    path('unidad/listar/', view_unidad.listar_unidad, name='listar_unidad'),
    #urls para reactivo_base
    path('reactivo/base/<int:pk>/', view_reactivo_base.base, name='base'),
    path('reactivo/base/crear/', view_reactivo_base.crear_base, name='crear_base'),
    path('reactivo/base/listar/', view_reactivo_base.listar_base, name='listar_base'),
    #urls para lugar
    path('lugar/<int:pk>/', view_lugar.lugar, name='lugar'),
    path('lugar/crear/', view_lugar.crear_lugar, name='crear_lugar'),
    path('lugar/listar/', view_lugar.listar_lugar, name='listar_lugar'),
    #urls para fase
    path('fase/<int:pk>/', view_fase.fase, name='fase'),
    path('fase/crear/', view_fase.crear_fase, name='crear_fase'),
    path('fase/listar/', view_fase.listar_fase, name='listar_fase'),
    #urls para codigo
    path('reactivo/codigo/<int:pk>/', view_codigo.codigo, name='codigo'),
    path('reactivo/codigo/crear/', view_codigo.crear_codigo, name='crear_codigo'),
    path('reactivo/codigo/listar/', view_codigo.listar_codigo, name='listar_codigo'),
    #urls para cantidad
    path('cantidad/<int:pk>/', view_cantidad.cantidad, name='cantidad'),
    path('cantidad/crear/', view_cantidad.crear_cantidad, name='crear_cantidad'),
    path('cantidad/listar/', view_cantidad.listar_cantidad, name='listar_cantidad'),
    #url para Consecutivo
    path('consecutivo/listar/', view_consecutivo.listar_consecutivo, name='listar_consecutivo'),
    #urls para consumo
    path('consumo/<int:pk>/', view_consumo.consumo, name='consumo'),
    path('consumo/crear/', view_consumo.crear_consumo, name='crear_consumo'),
    path('consumo/listar/', view_consumo.listar_consumo, name='listar_consumo')

]
