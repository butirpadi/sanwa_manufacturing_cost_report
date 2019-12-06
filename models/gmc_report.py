from odoo import fields, models, api, _
from odoo.exceptions import UserError
from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta


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
    production_amount_a_year = fields.Float(string="Production Amount")


    cost_of_material_used_amount = fields.Float(
        string="Cost of Material Used Amount")
    cost_of_material_used_amount_percent = fields.Float(
        string="Cost of Material Used Amount Percent")
    
    cost_of_material_used_amount_a_year = fields.Float(
        string="Cost of Material Used Amount")
    cost_of_material_used_amount_percent_a_year = fields.Float(
        string="Cost of Material Used Amount Percent")

    begining_material_stock_account_id = fields.Many2one(
        string='Begining Material Stock Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    begining_material_stock = fields.Float(string="Begining Material Stock")
    begining_material_stock_percent = fields.Float(
        string="Begining Material Stock Percent")
    
    begining_material_stock_a_year = fields.Float(string="Begining Material Stock")
    begining_material_stock_percent_a_year = fields.Float(
        string="Begining Material Stock Percent")

    material_net_purchased_account_id = fields.Many2one(
        string='Material Net Purchased Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    material_net_purchased = fields.Float(string="Materials Net Purchased")
    material_net_purchased_percent = fields.Float(
        string="Materials Net Purchased Percent")
    
    material_net_purchased_a_year = fields.Float(string="Materials Net Purchased")
    material_net_purchased_percent_a_year = fields.Float(
        string="Materials Net Purchased Percent")

    ending_material_stock_account_id = fields.Many2one(
        string='Ending Material Stock Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    ending_material_stock = fields.Float(string="Ending Material Stock")
    ending_material_stock_percent = fields.Float(
        string="Ending Material Stock Percent")
    
    ending_material_stock_a_year = fields.Float(string="Ending Material Stock")
    ending_material_stock_percent_a_year = fields.Float(
        string="Ending Material Stock Percent")

    material_adjustment_account_id = fields.Many2one(
        string='Material Adjustment Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    material_adjustment = fields.Float(string="Material Adjustments ETC")
    material_adjustment_percent = fields.Float(
        string="Material Adjustments ETC Percent")
    
    material_adjustment_a_year = fields.Float(string="Material Adjustments ETC")
    material_adjustment_percent_a_year = fields.Float(
        string="Material Adjustments ETC Percent")

    begining_work_in_process_account_id = fields.Many2one(
        string='Begining Work in Process Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    begining_work_in_process = fields.Float(string="Begining Work in Process")
    begining_work_in_process_percent = fields.Float(
        string="Begining Work in Process Percent")
    
    begining_work_in_process_a_year = fields.Float(string="Begining Work in Process")
    begining_work_in_process_percent_a_year = fields.Float(
        string="Begining Work in Process Percent")

    ending_work_in_process_account_id = fields.Many2one(
        string='Ending Work in Process Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    ending_work_in_process = fields.Float(string="Ending Work in Process")
    ending_work_in_process_percent = fields.Float(
        string="Ending Work in Process Percent")
    
    ending_work_in_process_a_year = fields.Float(string="Ending Work in Process")
    ending_work_in_process_percent_a_year = fields.Float(
        string="Ending Work in Process Percent")

    adjustment_account_id = fields.Many2one(
        string='Adjustment Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    adjustment = fields.Float(string="Adjustments")
    adjustment_percent = fields.Float(string="Adjustments Percent")
    
    adjustment_a_year = fields.Float(string="Adjustments")
    adjustment_percent_a_year = fields.Float(string="Adjustments Percent")

    process_cost_account_id = fields.Many2one(
        string='Process Cost Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    process_cost = fields.Float(string="Process Cost")
    process_cost_percent = fields.Float(string="Process Cost Percent")
    
    process_cost_a_year = fields.Float(string="Process Cost")
    process_cost_percent_a_year = fields.Float(string="Process Cost Percent")

    labor_cost = fields.One2many(
        string='Labor Cost',
        comodel_name='gmc.report.labor.cost.rel',
        inverse_name='gmc_report_id',
    )
    labor_cost_amount = fields.Float(string="Labor Cost Amount")
    labor_cost_amount_percent = fields.Float(
        string="Labor Cost Amount Percent")
    
    labor_cost_amount_a_year = fields.Float(string="Labor Cost Amount")
    labor_cost_amount_percent_a_year = fields.Float(
        string="Labor Cost Amount Percent")

    manufacture_expenses = fields.One2many(
        string='Labor Cost',
        comodel_name='gmc.report.manufacture.expense.rel',
        inverse_name='gmc_report_id',
    )
    manufacture_expenses_amount = fields.Float(
        string="Manufacturing Expenses Amount")
    manufacture_expenses_amount_percent = fields.Float(
        string="Manufacturing Expenses Amount Percent")
    
    manufacture_expenses_amount_a_year = fields.Float(
        string="Manufacturing Expenses Amount")
    manufacture_expenses_amount_percent_a_year = fields.Float(
        string="Manufacturing Expenses Amount Percent")

    def action_submit(self):
        # get report setting
        gmc_report_config = self.env['gmc.report.config'].search([], limit=1)

        # get one year
        current_year = datetime(self.date_from.year,self.env.user.company_id.fiscalyear_last_month,self.env.user.company_id.fiscalyear_last_day,0,0,0)
        delta = relativedelta(months=12)
        satu_tahun_lalu = current_year - delta

        self.production_amount_account_id = gmc_report_config.production_amount_account_id.id
        self.begining_material_stock_account_id = gmc_report_config.begining_material_stock_account_id.id
        self.material_net_purchased_account_id = gmc_report_config.material_net_purchased_account_id.id
        self.ending_material_stock_account_id = gmc_report_config.ending_material_stock_account_id.id
        self.material_adjustment_account_id = gmc_report_config.material_adjustment_account_id.id
        self.begining_work_in_process_account_id = gmc_report_config.begining_work_in_process_account_id.id
        self.ending_work_in_process_account_id = gmc_report_config.ending_work_in_process_account_id.id
        self.adjustment_account_id = gmc_report_config.adjustment_account_id.id
        self.process_cost_account_id = gmc_report_config.process_cost_account_id.id

        # get amount of production_amount
        prd_amt = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.production_amount_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.production_amount = sum(prd_amt.mapped(
            'debit')) - sum(prd_amt.mapped('credit'))
        
        prd_amt_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.production_amount_account_id.id),
                ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
             ])

        self.production_amount_a_year = sum(prd_amt_a_year.mapped(
            'debit')) - sum(prd_amt_a_year.mapped('credit'))

        # get amount of begining_material_stock
        bgn_mat_stk = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.begining_material_stock_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.begining_material_stock = sum(bgn_mat_stk.mapped(
            'debit')) - sum(bgn_mat_stk.mapped('credit'))
        
        if self.production_amount > 0:
            self.begining_material_stock_percent = self.begining_material_stock / \
                self.production_amount * 100
        else:
            self.begining_material_stock_percent = 0.0
        
        bgn_mat_stk_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.begining_material_stock_account_id.id),
                ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
             ])

        self.begining_material_stock_a_year = sum(bgn_mat_stk_a_year.mapped(
            'debit')) - sum(bgn_mat_stk_a_year.mapped('credit'))
        if self.production_amount_a_year > 0:
            self.begining_material_stock_percent_a_year = self.begining_material_stock_a_year / \
                self.production_amount_a_year * 100
        else:
            self.begining_material_stock_percent_a_year = 0.0

        # get amount of material_net_purchased
        mat_net_purch = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.material_net_purchased_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.material_net_purchased = sum(mat_net_purch.mapped(
            'debit')) - sum(mat_net_purch.mapped('credit'))
        if self.production_amount > 0:
            self.material_net_purchased_percent = self.material_net_purchased / \
                self.production_amount * 100
        else:
            self.material_net_purchased_percent = 0.0
        
        mat_net_purch_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.material_net_purchased_account_id.id),
                ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
             ])

        self.material_net_purchased_a_year = sum(mat_net_purch_a_year.mapped(
            'debit')) - sum(mat_net_purch_a_year.mapped('credit'))
        if self.production_amount_a_year > 0:
            self.material_net_purchased_percent_a_year = self.material_net_purchased_a_year / \
                self.production_amount_a_year * 100
        else:
            self.material_net_purchased_percent_a_year = 0

        # get amount of material_net_purchased
        end_mat_stk = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.ending_material_stock_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.ending_material_stock = sum(end_mat_stk.mapped(
            'debit')) - sum(end_mat_stk.mapped('credit'))
        if self.production_amount > 0:
            self.ending_material_stock_percent = self.ending_material_stock / \
            self.production_amount * 100
        else:
            self.ending_material_stock_percent = 0.0
        
        end_mat_stk_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.ending_material_stock_account_id.id),
                ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
             ])

        self.ending_material_stock_a_year = sum(end_mat_stk_a_year.mapped(
            'debit')) - sum(end_mat_stk_a_year.mapped('credit'))
        if self.production_amount_a_year > 0:
            self.ending_material_stock_percent_a_year = self.ending_material_stock_a_year / \
            self.production_amount_a_year * 100
        else:
            self.ending_material_stock_percent_a_year = 0

        # get amount of material_adjustment
        mat_adj = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.material_adjustment_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.material_adjustment = sum(mat_adj.mapped(
            'debit')) - sum(mat_adj.mapped('credit'))
        if self.production_amount > 0:
            self.material_adjustment_percent = self.material_adjustment / \
                self.production_amount * 100
        else:
            self.material_adjustment_percent = 0.0
        
        mat_adj_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.material_adjustment_account_id.id),
                ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
             ])

        self.material_adjustment_a_year = sum(mat_adj_a_year.mapped(
            'debit')) - sum(mat_adj_a_year.mapped('credit'))
        if self.production_amount_a_year > 0:
            self.material_adjustment_percent_a_year = self.material_adjustment_a_year / \
            self.production_amount_a_year * 100
        else:
            self.material_adjustment_percent_a_year = 0

        # get amount of begining wip
        bgn_wip = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.begining_work_in_process_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.begining_work_in_process = sum(bgn_wip.mapped(
            'debit')) - sum(bgn_wip.mapped('credit'))
        if self.production_amount > 0:
            self.begining_work_in_process_percent = self.begining_work_in_process / \
            self.production_amount * 100
        else:
            self.begining_work_in_process_percent = 0.0
        
        bgn_wip_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.begining_work_in_process_account_id.id),
                ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
             ])

        self.begining_work_in_process_a_year = sum(bgn_wip_a_year.mapped(
            'debit')) - sum(bgn_wip_a_year.mapped('credit'))
        if self.production_amount_a_year > 0:
            self.begining_work_in_process_percent_a_year = self.begining_work_in_process_a_year / \
            self.production_amount_a_year * 100
        else:
            self.begining_work_in_process_percent_a_year = 0

        # get amount of ending wip
        end_wip = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.ending_work_in_process_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.ending_work_in_process = sum(end_wip.mapped(
            'debit')) - sum(end_wip.mapped('credit'))
        if self.production_amount > 0:
            self.ending_work_in_process_percent = self.ending_work_in_process / \
            self.production_amount * 100
        else:
            self.ending_work_in_process_percent = 0.0
        
        end_wip_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.ending_work_in_process_account_id.id),
                ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
             ])

        self.ending_work_in_process_a_year = sum(end_wip_a_year.mapped(
            'debit')) - sum(end_wip_a_year.mapped('credit'))

        if self.production_amount_a_year > 0:
            self.ending_work_in_process_percent_a_year = self.ending_work_in_process_a_year / \
            self.production_amount_a_year * 100
        else:
            self.ending_work_in_process_percent_a_year = 0

        # get amount of adjustment
        adjs = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.adjustment_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.adjustment = sum(adjs.mapped(
            'debit')) - sum(adjs.mapped('credit'))
        if self.production_amount > 0:
            self.adjustment_percent = self.adjustment / self.production_amount * 100
        else:
            self.adjustment_percent = 0.0
        
        adjs_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.adjustment_account_id.id),
                ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
             ])

        self.adjustment_a_year = sum(adjs_a_year.mapped(
            'debit')) - sum(adjs_a_year.mapped('credit'))
        if self.production_amount_a_year > 0:
            self.adjustment_percent_a_year = self.adjustment_a_year / self.production_amount_a_year * 100
        else:
            self.adjustment_percent_a_year = 0


        # get amount of process cost
        proc_cost = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.process_cost_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.process_cost = sum(proc_cost.mapped(
            'debit')) - sum(proc_cost.mapped('credit'))
        if self.production_amount > 0:
            self.process_cost_percent = self.process_cost / self.production_amount * 100
        else:
            self.process_cost_percent = 0
        
        proc_cost_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.process_cost_account_id.id),
                ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
             ])

        self.process_cost_a_year = sum(proc_cost_a_year.mapped(
            'debit')) - sum(proc_cost_a_year.mapped('credit'))
        if self.production_amount_a_year > 0:
            self.process_cost_percent_a_year = self.process_cost_a_year / self.production_amount_a_year * 100
        else:
            self.process_cost_percent_a_year = 0

        # --------------------------------------------------------------

        self.cost_of_material_used_amount = self.begining_material_stock + \
            self.material_net_purchased - self.ending_material_stock - self.material_adjustment
        if self.production_amount > 0:
            self.cost_of_material_used_amount_percent = self.cost_of_material_used_amount / \
            self.production_amount * 100
        else:
            self.cost_of_material_used_amount_percent = 0
        
        self.cost_of_material_used_amount_a_year = self.begining_material_stock_a_year + \
            self.material_net_purchased_a_year - self.ending_material_stock_a_year - self.material_adjustment_a_year
        if self.production_amount_a_year > 0:
            self.cost_of_material_used_amount_percent_a_year = self.cost_of_material_used_amount_a_year / \
            self.production_amount_a_year * 100
        else:
            self.cost_of_material_used_amount_percent_a_year = 0

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

            if self.production_amount > 0:
                acc_percent = acc_amount / self.production_amount * 100
            else:
                acc_percent = 0


            # get account move line from this account
            acc_amls_a_year = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
                 ])
            # get amount from those account move lines
            acc_amount_a_year = sum(acc_amls_a_year.mapped('debit')) - \
                sum(acc_amls_a_year.mapped('credit'))

            if self.production_amount_a_year > 0:
                acc_percent_a_year = acc_amount_a_year / self.production_amount_a_year * 100
            else:
                acc_percent_a_year = 0

            labor_cost_ids.append((0, 0, {
                'account_id': acc.id,
                'account_value': acc_amount,
                'account_percent': acc_percent,
                'account_value_a_year': acc_amount_a_year,
                'account_percent_a_year': acc_percent_a_year,
            }))

        self.labor_cost.unlink()
        self.labor_cost = labor_cost_ids

        self.labor_cost_amount = sum(self.labor_cost.mapped('account_value'))

        if self.production_amount > 0:
            self.labor_cost_amount_percent = self.labor_cost_amount / self.production_amount * 100
        else:
            self.labor_cost_amount_percent = 0
        
        self.labor_cost_amount_a_year = sum(self.labor_cost.mapped('account_value_a_year'))
        if self.production_amount_a_year > 0:
            self.labor_cost_amount_percent_a_year = self.labor_cost_amount_percent_a_year / self.production_amount_a_year * 100
        else:
            self.labor_cost_amount_percent_a_year = 0

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

            if self.production_amount > 0:
                acc_percent = acc_amount / self.production_amount * 100
            else:
                acc_percent = 0            
            
            acc_amls_a_year = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date_maturity', '>', satu_tahun_lalu),
                ('date_maturity', '<=', current_year)
                 ])
            # get amount from those account move lines
            acc_amount_a_year = sum(acc_amls_a_year.mapped('debit')) - \
                sum(acc_amls_a_year.mapped('credit'))

            if self.production_amount_a_year > 0:
                acc_percent_a_year = acc_amount_a_year / self.production_amount_a_year * 100
            else:
                acc_percent_a_year = 0


            man_exp_ids.append((0, 0, {
                'account_id': acc.id,
                'account_value': acc_amount,
                'account_percent': acc_percent,
                'account_value_a_year': acc_amount_a_year,
                'account_percent_a_year': acc_percent_a_year,
            }))

        self.manufacture_expenses.unlink()
        self.manufacture_expenses = man_exp_ids

        self.manufacture_expenses_amount = sum(
            self.manufacture_expenses.mapped('account_value'))
        if self.production_amount > 0:
            self.manufacture_expenses_amount_percent = self.manufacture_expenses_amount / \
                self.production_amount * 100
        else:
            self.manufacture_expenses_amount_percent = 0
        
        self.manufacture_expenses_amount_a_year = sum(
            self.manufacture_expenses.mapped('account_value_a_year'))
        if self.production_amount_a_year > 0:
            self.manufacture_expenses_amount_percent_a_year = self.manufacture_expenses_amount_a_year / \
            self.production_amount_a_year * 100
        else:
            self.manufacture_expenses_amount_percent_a_year = 0
        
        # get fiscal year last month and day
        print('Get Fiscal Year Last Month & day')
        # print(self.env.user.company_id.fiscalyear_last_month)
        # print(self.env.user.company_id.fiscalyear_last_day)
        
        # first_day_a_year_str = str(self.date_from.year) + '-' + str(self.env.user.company_id.fiscalyear_last_month-11) + '-' + '01 00:00:00.243860'
        # first_day_a_year_obj = datetime.strptime(first_day_a_year_str, '%Y-%m-%d %H:%M:%S.%f')

        # last_day_a_year_str = str(self.date_from.year) + '-' + str(self.env.user.company_id.fiscalyear_last_month) + '-' + str(self.env.user.company_id.fiscalyear_last_day) + ' 00:00:00.243860'
        # last_day_a_year_obj = datetime.strptime(last_day_a_year_str, '%Y-%m-%d %H:%M:%S.%f')

        # # print(first_day_a_year_obj.date())
        # print(last_day_a_year_obj.date())

        

        return self.env.ref('sanwa_manufacturing_cost_report.gross_manufacturing_cost_report_action').report_action(self)
