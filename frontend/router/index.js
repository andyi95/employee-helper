import {createRouter, createWebHistory} from 'vue-router'

import Main from "@/pages/Main.vue";

const routes = [
  {path: '/', name: 'Main', component: Main, meta: {title: "Вакансии"}},
  {path: '/:catchAll(.*)', redirect: '/'}

]
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  linkActiveClass: 'active',
  routes
});
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? to.meta.title : "Кабинет соискателя"
  next()
})

export default router

