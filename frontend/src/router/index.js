import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    children: [
      {
        path: 'alumni-info',
        name: 'AlumniInfo',
        component: () => import('../views/alumni/AlumniInfo.vue')
      },
      {
        path: 'alumni-applications',
        name: 'AlumniApplications',
        component: () => import('../views/alumni/AlumniApplications.vue')
      },
      {
        path: 'alumni-statistics',
        name: 'AlumniStatistics',
        component: () => import('../views/alumni/AlumniStatistics.vue')
      },
      {
        path: 'my-info',
        name: 'MyInfo',
        component: () => import('../views/alumni/AlumniInfo.vue')
      },
      {
        path: 'career-recommendations',
        name: 'CareerRecommendations',
        component: () => import('../views/alumni/CareerRecommendations.vue')
      },
      {
        path: 'association-manage',
        name: 'AssociationManage',
        component: () => import('../views/admin/AssociationManage.vue'),
        meta: {
          requiresAuth: true,
          roles: ['admin']
        }
      },
      {
        path: 'branch-manage',
        name: 'AssociationBranch',
        component: () => import('../views/admin/AssociationBranchManage.vue'),
        meta: {
          requiresAuth: true,
          roles: ['admin']
        }
      },
      {
        path: 'association-overview',
        name: 'AssociationOverview',
        component: () => import('../views/liaison/AssociationOverview.vue'),
        meta: {
          requiresAuth: true,
          roles: ['liaison']
        }
      },
      {
        path: 'association-members',
        name: 'AssociationMembers',
        component: () => import('../views/liaison/AssociationMembers.vue'),
        meta: {
          requiresAuth: true,
          roles: ['liaison']
        }
      },
      {
        path: 'application-approval',
        name: 'ApplicationApproval',
        component: () => import('../views/liaison/ApplicationApproval.vue'),
        meta: {
          requiresAuth: true,
          roles: ['liaison']
        }
      },
      {
        path: 'join-association',
        name: 'JoinAssociation',
        component: () => import('../views/alumni/JoinAssociation.vue'),
        meta: {
          requiresAuth: true,
          roles: ['alumni']
        }
      },
      {
        path: 'my-association',
        name: 'MyAssociation',
        component: () => import('../views/alumni/MyAssociation.vue'),
        meta: {
          requiresAuth: true,
          roles: ['alumni']
        }
      },
        {
        path: 'activity-publish',
        name: 'ActivityPublish',
        component: () => import('@/views/liaison/ActivityPublish.vue'),
        meta: {
          title: '活动发布',
          roles: ['liaison']  // 只允许校友联络员访问
        }
      },
      {
        path: 'activity-approval',
        name: 'ActivityApproval',
        component: () => import('../views/admin/ActivityApproval.vue'),
        meta: {
          title: '活动审批',
          roles: ['admin']
        }
      },
      {
        path: 'activity-registration',
        name: 'ActivityRegistration',
        component: () => import('../views/alumni/ActivityRegistration.vue'),
        meta: {
          title: '活动报名',
          roles: ['graduated_alumni']
        }
      },
      {
        path: 'my-activities',
        name: 'MyActivities',
        component: () => import('@/views/alumni/MyActivities.vue'),
        meta: {
          title: '我的活动',
          requiresAuth: true,
          roles: ['graduated_alumni']
        }
      },
      {
        path: 'holiday-greetings',
        name: 'Greeting',
        component: () => import('@/views/admin/Greetings.vue'),
        meta: {
          title: '节日祝福',
          requiresAuth: true,
          roles: ['admin', 'liaison']
        }
      },
      {
        path: 'news-notice',
        name: 'New',
        component: () => import('@/views/admin/News.vue'),
        meta: {
          title: '新闻通知',
          requiresAuth: true,
          roles: ['admin', 'liaison']
        }
      },
      {
        path: 'activity-notice',
        name: 'Activity',
        component: () => import('@/views/admin/Activities.vue'),
        meta: {
          title: '活动通知',
          requiresAuth: true,
          roles: ['admin', 'liaison']
        }
      },
        {
        path: 'holiday-greetings-graduate',
        name: 'Greetings',
        component: () => import('@/views/alumni/Greetings.vue'),
        meta: {
          title: '节日祝福',
          requiresAuth: true,
          roles: ['graduated_alumni']
        }
      },
      {
        path: 'news-notice-graduate',
        name: 'News',
        component: () => import('@/views/alumni/News.vue'),
        meta: {
          title: '新闻通知',
          requiresAuth: true,
          roles: ['graduated_alumni']
        }
      },
      {
        path: 'activity-notice-graduate',
        name: 'Activities',
        component: () => import('@/views/alumni/Activities.vue'),
        meta: {
          title: '活动通知',
          requiresAuth: true,
          roles: ['graduated_alumni']
        }
      },
      {
        path: 'activity-recommendations',
        name: 'ActivityPlanning',
        component: () => import('@/views/liaison/ActivityPlanning.vue'),
        meta: {
          title: '活动策划推荐',
          requiresAuth: true,
          roles: ['liaison']
        }
      },
      {
        path: 'donation-projects',
        name: 'DonationProjects',
        component: () => import('@/views/alumni/DonationProjects.vue'),
        meta: { title: '回馈母校' }
      },
      {
        path: 'council-meeting',
        name: 'CouncilMeeting',
        component: () => import('@/views/liaison/CouncilMeeting.vue'),
        meta: {
          title: '理事会召开',
          requiresAuth: true,
          roles: ['liaison']
        }
      },
      {
        path: 'council-overview',
        name: 'CouncilOverview',
        component: () => import('@/views/liaison/CouncilOverview.vue'),
        meta: {
          title: '理事会概况',
          requiresAuth: true,
          roles: ['liaison']
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = store.state.token
  
  if (to.path === '/login') {
    if (token) {
      next('/dashboard')
    } else {
      next()
    }
  } else {
    if (token) {
      next()
    } else {
      next('/login')
    }
  }
})

export default router 