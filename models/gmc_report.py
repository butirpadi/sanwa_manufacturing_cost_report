from odoo import fields, models, api, _
from odoo.exceptions import UserError
from pprint import pprint


class GmcReport(models.TransientModel):
    _name = 'gmc.report'
    _description = 'Gross Manufacture Report'

    name = fields.Char(string='Name', default="Gross Manufacture Cost Report")
    date_from = fields.Date(string="Date start")
    date_to = fields.Date(string="Date to")

    production_amount_account_id = fields.Many2one(
        string='Production Amount Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    production_amount = fields.Float(string="Production Amount")

    begining_material_stock_account_id = fields.Many2one(
        string='Begining Material Stock Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    begining_material_stock = fields.Float(string="Begining Material Stock")

    material_net_purchased_account_id = fields.Many2one(
        string='Material Net Purchased Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    material_net_purchased = fields.Float(string="Materials Net Purchased")

    ending_material_stock_account_id = fields.Many2one(
        string='Ending Material Stock Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    ending_material_stock = fields.Float(string="Ending Material Stock")

    material_adjustment_account_id = fields.Many2one(
        string='Material Adjustment Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    material_adjustment = fields.Float(string="Material Adjustments ETC")

    begining_work_in_process_account_id = fields.Many2one(
        string='Begining Work in Process Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    begining_work_in_process = fields.Float(string="Begining Work in Process")

    ending_work_in_process_account_id = fields.Many2one(
        string='Ending Work in Process Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    ending_work_in_process = fields.Float(string="Ending Work in Process")

    adjustment_account_id = fields.Many2one(
        string='Adjustment Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    adjustment = fields.Float(string="Adjustments")

    process_cost_account_id = fields.Many2one(
        string='Process Cost Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    process_cost = fields.Float(string="Process Cost")

    labor_cost = fields.One2many(
        string='Labor Cost',
        comodel_name='gmc.report.labor.cost.rel',
        inverse_name='gmc_report_id',
    )
    labor_cost_amount = fields.Float(string="Labor Cost Amount")

    manufacture_expenses = fields.One2many(
        string='Labor Cost',
        comodel_name='gmc.report.manufacture.expense.rel',
        inverse_name='gmc_report_id',
    )
    manufacture_expenses_amount = fields.Float(
        string="Manufacturing Expenses Amount")

    def action_submit(self):
        # get report setting
        gmc_report_config = self.env['gmc.report.config'].search([], limit=1)

        self.production_amount_account_id = gmc_report_config.production_amount_account_id.id
        self.begining_material_stock_account_id = gmc_report_config.begining_material_stock_account_id.id
        self.material_net_purchased_account_id = gmc_report_config.material_net_purchased_account_id.id
        self.ending_material_stock_account_id = gmc_report_config.ending_material_stock_account_id.id
        self.material_adjustment_account_id = gmc_report_config.material_adjustment_account_id.id
        self.begining_work_in_process_account_id = gmc_report_config.begining_work_in_process_account_id.id
        self.ending_work_in_process_account_id = gmc_report_config.ending_work_in_process_account_id.id
        self.adjustment_account_id = gmc_report_config.adjustment_account_id.id
        self.process_cost_account_id = gmc_report_config.process_cost_account_id.id
        # self.labor_cost =  [(4, gmc_report_config.labor_cost_account_ids.ids)]
        # self.manufacture_expenses = [(4, gmc_report_config.manufacturing_expense_account_ids.ids)],

        # get amount of production_amount
        prd_amt = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.production_amount_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.production_amount = sum(prd_amt.mapped(
            'debit')) - sum(prd_amt.mapped('credit'))

        # get amount of begining_material_stock
        bgn_mat_stk = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.begining_material_stock_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.begining_material_stock = sum(bgn_mat_stk.mapped(
            'debit')) - sum(bgn_mat_stk.mapped('credit'))

        # get amount of material_net_purchased
        mat_net_purch = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.material_net_purchased_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.material_net_purchased = sum(mat_net_purch.mapped(
            'debit')) - sum(mat_net_purch.mapped('credit'))

        # get amount of material_net_purchased
        end_mat_stk = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.ending_material_stock_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.ending_material_stock = sum(end_mat_stk.mapped(
            'debit')) - sum(end_mat_stk.mapped('credit'))

        # get amount of material_adjustment
        mat_adj = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.material_adjustment_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.material_adjustment = sum(mat_adj.mapped(
            'debit')) - sum(mat_adj.mapped('credit'))

        # get amount of begining wip
        bgn_wip = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.begining_work_in_process_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.begining_work_in_process = sum(bgn_wip.mapped(
            'debit')) - sum(bgn_wip.mapped('credit'))

        # get amount of ending wip
        end_wip = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.ending_work_in_process_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.ending_work_in_process = sum(end_wip.mapped(
            'debit')) - sum(end_wip.mapped('credit'))

        # get amount of adjustment
        adjs = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.adjustment_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.adjustment = sum(adjs.mapped(
            'debit')) - sum(adjs.mapped('credit'))

        # get amount of process cost
        proc_cost = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.process_cost_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.adjustment = sum(proc_cost.mapped(
            'debit')) - sum(proc_cost.mapped('credit'))

        # --------------------------------------------------------------

        print('get labor cost')
        labor_cost_ids = []
        for acc in gmc_report_config.labor_cost_account_ids:

            # get account move line from this account
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date_maturity', '>=', self.date_from),
                 ('date_maturity', '<=', self.date_to)
                 ])
            # get amount from those account move lines
            acc_amount = sum(acc_amls.mapped('debit')) - \
                sum(acc_amls.mapped('credit'))

            labor_cost_ids.append((0, 0, {
                'account_id': acc.id,
                'account_value': acc_amount
            }))

        self.labor_cost.unlink()
        self.labor_cost = labor_cost_ids
        self.labor_cost_amount = sum(self.labor_cost.mapped('account_value'))

        man_exp_ids = []
        for acc in gmc_report_config.manufacturing_expense_account_ids:
            # get account move line from this account
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date_maturity', '>=', self.date_from),
                 ('date_maturity', '<=', self.date_to)
                 ])
            # get amount from those account move lines
            acc_amount = sum(acc_amls.mapped('debit')) - \
                sum(acc_amls.mapped('credit'))

            man_exp_ids.append((0, 0, {
                'account_id': acc.id,
                'account_value': acc_amount
            }))

        self.manufacture_expenses.unlink()
        self.manufacture_expenses = man_exp_ids
        self.manufacture_expenses_amount = sum(self.manufacture_expenses.mapped('account_value'))

        return self.env.ref('sanwa_manufacturing_cost_report.gross_manufacturing_cost_report_action').report_action(self) 


