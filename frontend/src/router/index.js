import { createRouter, createWebHistory } from 'vue-router'

import AuthLayout from '@/layouts/AuthLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import AccountLayout from '@/layouts/AccountLayout.vue'

import LoginView from '@/views/Auth/LoginView.vue'
import RegisterView from '@/views/Auth/RegisterView.vue'
import AdminUsersView from '@/views/Admin/AdminUsersView.vue'
import HomeView from '@/views/HomeView.vue'
import ChangeEmailView from '@/views/Account/ChangeEmailView.vue'
import ChangePasswordView from '@/views/Account/ChangePasswordView.vue'
import ChangeProfileView from '@/views/Account/ChangeProfileView.vue'
import UserInfoView from '@/views/Account/UserInfoView.vue'


// index.jsというファイル名について、Vite や Webpack などのフロントエンドの開発ツールでは、慣例的に、
// フォルダをモジュールとして指定した際のデフォルトのエントリーポイントとしてこの名前のファイルを扱う。
// Pythonの__init__.pyと同様に、フォルダ内の各モジュールから必要なものをインポートし、
// まとめてexportする「窓口」として index.js が使われる

const routes = [
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
        component: RegisterView
      },

      {
        path: 'login',
        name: 'login',
        component: LoginView
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
        component: ChangeEmailView
      },
      {
        path: 'change-password',
        name: 'change-password',
        component: ChangePasswordView
      },
      {
        path: 'change-profile',
        name: 'change-profile',
        component: ChangeProfileView
      },
      {
        path: 'user-info',
        name: 'user-info',
        component: UserInfoView
      },
    ]

  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminLayout,
    children: [
      {
        path: 'users',
        name: 'admin-users',
        component: AdminUsersView,
      },
    ]
  }

]



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
