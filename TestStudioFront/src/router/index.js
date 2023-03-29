import Vue from 'vue'
import VueRouter from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import LayOut from '../views/LayOut.vue'
import TestTask from '../views/TestTask.vue'
import TestReport from '../views/TestReport.vue'
import CaseTree from '../views/CaseTree.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: "layout"
    // name: 'home',
    // component: HomeView
  },
  {
    path: '/layout',
    name: 'layout',
    component: LayOut,
    children: [
      {
        path: "casetree",
        name: 'casetree',
        component: CaseTree
      },
      {
        path: "testtask",
        name: 'testtask',
        component: TestTask
      },
      {
        path: "testreport",
        name: 'testreport',
        component: TestReport
      },
    ]
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
