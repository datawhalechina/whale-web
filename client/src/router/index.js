import Vue from 'vue';
import VueRouter from 'vue-router';
import Layout from '@/layout';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Layout,
    redirect: '/articles',
    children: [
      {
        path: 'articles',
        name: 'articles',
        redirect: '/articles/list',
        component: () => import('../views/Articles.vue'),
        children: [
          {
            path: 'list',
            component: () => import('../views/ArticleList.vue'),
          },
          {
            path: 'detail/:id',
            component: () => import('../views/ArticleDetail.vue'),
          },
          {
            path: 'editor/:id',
            component: () => import('../views/ArticleEditor.vue'),
          },
        ],
      },
      {
        path: 'qa',
        name: 'qa',
        component: () => import('../views/QA.vue'),
      },
      {
        path: 'subscribes',
        name: 'subscribes',
        component: () => import('../views/Subscribes.vue'),
      },
      {
        path: 'login',
        name: 'login',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue'),
      },
      {
        path: 'register',
        name: 'register',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "register" */ '../views/Register.vue'),
      },
    ],
  },
  {
    path: '/verify/:token',
    name: 'verifyToken',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "verify" */ '../views/VerifyToken.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
