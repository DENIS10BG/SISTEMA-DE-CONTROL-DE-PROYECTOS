import { createRouter, createWebHistory } from 'vue-router'
import Inicio_Principal from '../views/Inicio_Principal.vue'
import Login_Principal from '../views/Login_Principal.vue'
import Panel_Principal from '../views/Panel_Principal.vue'
import PanelLayout from '../layouts/PanelLayout.vue'
import PanelUsuarios from '../views/panel/PanelUsuarios.vue'
import PanelUsuarioVer from '../views/panel/PanelUsuarioVer.vue'
import PanelUsuarioEditar from '../views/panel/PanelUsuarioEditar.vue'
import PanelUsuarioNuevo from '../views/panel/PanelUsuarioNuevo.vue'
import PanelProyectos from '../views/panel/PanelProyectos.vue'
import PanelProcesamiento from '../views/panel/PanelProcesamiento.vue'
import PanelReportes from '../views/panel/PanelReportes.vue'
import PanelAlertas from '../views/panel/PanelAlertas.vue'
import PanelAsistente from '../views/panel/PanelAsistente.vue'
import PanelPerfil from '../views/panel/PanelPerfil.vue'
import PanelAjustes from '../views/panel/PanelAjustes.vue'
import PanelProyectoDetalle from '../views/panel/PanelProyectoDetalle.vue'
import PanelAlertaDetalle from '../views/panel/PanelAlertaDetalle.vue'
import PanelAsistenteDetalle from '../views/panel/PanelAsistenteDetalle.vue'
import PanelProcesamientoVariante from '../views/panel/PanelProcesamientoVariante.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Inicio_Principal,
    },
    {
      path: '/login',
      name: 'login',
      component: Login_Principal,
    },
    {
      path: '/panel',
      component: PanelLayout,
      children: [
        {
          path: '',
          redirect: '/panel/general',
        },
        {
          path: 'general',
          name: 'panel-general',
          component: Panel_Principal,
        },
        {
          path: 'usuarios',
          name: 'panel-usuarios',
          component: PanelUsuarios,
        },
        {
          path: 'usuarios/ver',
          name: 'panel-usuario-ver',
          component: PanelUsuarioVer,
        },
        {
          path: 'usuarios/editar',
          name: 'panel-usuario-editar',
          component: PanelUsuarioEditar,
        },
        {
          path: 'usuarios/nuevo',
          name: 'panel-usuario-nuevo',
          component: PanelUsuarioNuevo,
        },
        {
          path: 'proyectos',
          name: 'panel-proyectos',
          component: PanelProyectos,
        },
        {
          path: 'procesamiento',
          name: 'panel-procesamiento',
          component: PanelProcesamiento,
        },
        {
          path: 'procesamiento/subir',
          name: 'panel-procesamiento-subir',
          component: PanelProcesamientoVariante,
        },
        {
          path: 'procesamiento/procesar',
          name: 'panel-procesamiento-procesar',
          component: PanelProcesamientoVariante,
        },
        {
          path: 'procesamiento/buscar',
          name: 'panel-procesamiento-buscar',
          component: PanelProcesamientoVariante,
        },
        {
          path: 'reportes',
          name: 'panel-reportes',
          component: PanelReportes,
        },
        {
          path: 'alertas',
          name: 'panel-alertas',
          component: PanelAlertas,
        },
        {
          path: 'asistente',
          name: 'panel-asistente',
          component: PanelAsistente,
        },
        {
          path: 'proyectos/detalle',
          name: 'panel-proyecto-detalle',
          component: PanelProyectoDetalle,
        },
        {
          path: 'alertas/detalle',
          name: 'panel-alerta-detalle',
          component: PanelAlertaDetalle,
        },
        {
          path: 'asistente/detalle',
          name: 'panel-asistente-detalle',
          component: PanelAsistenteDetalle,
        },
        {
          path: 'perfil',
          name: 'panel-perfil',
          component: PanelPerfil,
        },
        {
          path: 'ajustes',
          name: 'panel-ajustes',
          component: PanelAjustes,
        },
      ],
    },
  ],
})

export default router
