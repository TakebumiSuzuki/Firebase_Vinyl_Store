import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

import AuthLayout from '@/layouts/AuthLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import AccountLayout from '@/layouts/AccountLayout.vue'

import LoginView from '@/views/Auth/LoginView.vue'
import RegisterView from '@/views/Auth/RegisterView.vue'
import AdminUsersListView from '@/views/Admin/AdminUsersListView.vue'
import AdminUserDetailView from '@/views/Admin/AdminUserDetailView.vue'
import HomeView from '@/views/HomeView.vue'
import ChangeEmailView from '@/views/Account/ChangeEmailView.vue'
import ChangePasswordView from '@/views/Account/ChangePasswordView.vue'
import ChangeProfileView from '@/views/Account/ChangeProfileView.vue'
import UserInfoView from '@/views/Account/UserInfoView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import AccessDeniedView from '@/views/AccessDeniedView.vue'




function redirect_to_home(){
  const authStore = useAuthStore()
  if (authStore.isLoggedIn){
    return {name:'home'}
  }
  return true
}


// index.jsというファイル名について、Vite や Webpack などのフロントエンドの開発ツールでは、慣例的に、
// フォルダをモジュールとして指定した際のデフォルトのエントリーポイントとしてこの名前のファイルを扱う。
// Pythonの__init__.pyと同様に、フォルダ内の各モジュールから必要なものをインポートし、
// まとめてexportする「窓口」として index.js が使われる

const routes = [
  {
    path: '/',
    name: 'root',
    redirect: '/home'  // または適切なデフォルトページへリダイレクト
  },
  {
    path:'/home',
    name: 'home',
    component: HomeView,
  },

  {
    path: '/auth',
    name: 'auth', //直接 /auth や /admin に遷移させたい or 判定に使いたい場合のみ親に名前をつける意味あるとのこと。
    component: AuthLayout,
    children: [

      {
        path: 'register',
        name: 'register',
        component: RegisterView,
        beforeEnter: redirect_to_home
      },

      {
        path: 'login',
        name: 'login',
        component: LoginView,
        beforeEnter: redirect_to_home
      },

    ]
  },
  {
    path: '/account',
    name: 'account',
    component: AccountLayout,
    children:[
      {
        path: 'change-email',
        name: 'change-email',
        component: ChangeEmailView,
        meta: { loginRequired: true }
      },
      {
        path: 'change-password',
        name: 'change-password',
        component: ChangePasswordView,
        meta: { loginRequired: true }
      },
      {
        path: 'change-profile',
        name: 'change-profile',
        component: ChangeProfileView,
        meta: { loginRequired: true }
      },
      {
        path: 'user-info',
        name: 'user-info',
        component: UserInfoView,
        meta: { loginRequired: true }
      },
    ]

  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminLayout,
    children: [
      {
        path: 'users-list',
        name: 'admin-users-list',
        component: AdminUsersListView,
        meta: { loginRequired: true, adminRequired: true }
      },
      {
        path: 'user-detail/:uid',
        name: 'admin-user-detail',
        component: AdminUserDetailView,
        props: true,
        meta: { loginRequired: true, adminRequired: true }
      },
    ]
  },
  {
    path: '/access-denied',
    name: 'access-denied',
    component: AccessDeniedView,
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView
  },

]



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to)=>{
  if (to.meta.loginRequired){
    const authStore = useAuthStore()
    // JSでは、オブジェクトに存在しないキーへアクセスしようとすると、エラーにはならず、 undefined が返される。
    if (!authStore.isLoggedIn){
      return {name:'login'}
    }
    if (to.meta.adminRequired){
      if (!authStore.isAdmin){
        return {name: 'access-denied'}
      }
    }
  }
  return true


})


export default router
