import { createRouter, createWebHistory } from 'vue-router';
import Account from '@/components/user/account.vue';
import NotFound from '@/components/NotFound.vue';
import external_routes from '@/components/external/routes/index.js';
import internal_routes from '@/components/internal/routes/index.js';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/firsttime',
            name: 'first-time',
            component: Account,
        },
        {
            path: '/ledger-ui/accounts',
            name: 'account',
            component: Account,
        },
        external_routes,
        internal_routes,
        {
            path: '/:pathMatch(.*)*',
            name: 'not-found',
            component: NotFound,
        },
    ],
});

export default router;
