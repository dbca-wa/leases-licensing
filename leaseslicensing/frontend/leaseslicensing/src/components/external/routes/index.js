import ExternalDashboard from '@/components/external/dashboard.vue'
import Proposal from '@/components/external/proposal.vue'
import ProposalApply from '@/components/external/proposal_apply.vue'
import ProposalSubmit from '@/components/external/proposal_submit.vue'
import Organisation from '@/components/external/organisations/manage.vue'
import Compliance from '../compliances/access.vue'
import ComplianceSubmit from '../compliances/submit.vue'
/*
import Compliance from '../compliances/access.vue'
import ComplianceSubmit from '../compliances/submit.vue'
import Approval from '../approvals/approval.vue'
*/
export default
{
    path: '/external',
    component:
    {
        render(c)
        {
            return c('router-view')
        }
    },
    children: [
        {
            path: '/',
            component: ExternalDashboard,
            name: 'external-dashboard'
        },
        {
            path: 'organisations/manage/:org_id',
            component: Organisation
        },
        {
            path: 'compliance/:compliance_id',
            component: Compliance
        },
        {
            path: 'compliance/submit',
            component: ComplianceSubmit,
            name:"submit_compliance"
        },
        /*
        {
            path: 'approval/:approval_id',
            component: Approval,
        },
        */
        {
            path: 'proposal',
            component:
            {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: '/',
                    component: ProposalApply,
                    name:"apply_proposal"
                },
                {
                    path: 'submit',
                    component: ProposalSubmit,
                    name:"submit_proposal"
                },
                {
                    path: ':proposal_id',
                    component: Proposal,
                    name:"draft_proposal"
                },
            ]
        },
    ]
}
