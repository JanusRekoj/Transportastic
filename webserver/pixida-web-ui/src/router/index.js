import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue') // Allow lazy loading
    },
    {
        path: '/team',
        name: 'Team',
        component: () => import('../views/About.vue') // Allow lazy loading
    },
    {
        path: '/company',
        name: 'Company',
        component: () => import('../views/UseCase.vue') // Allow lazy loading
    },
    {
        path: '/passenger',
        name: 'Passenger',
        component: () => import('../views/Passenger.vue') // Allow lazy loading
    },
]

const router = new VueRouter({
    // mode: 'history',
    routes: routes
})

export default router
