from odoo import api, fields, models
from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta


class OperatingExpenseReport(models.TransientModel):
    _name = 'operating.expense.report'

    name = fields.Char(string='Name', default='Operating Expenses Report')
    date_from = fields.Date(string="Date start")
    date_to = fields.Date(string="Date to")

    net_sales_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Net Sales Account',
        ondelete='cascade'
    )
    net_sales_amount = fields.Float('Net Sales Amount')
    net_sales_amount_a_year = fields.Float('Net Sales Amount')

    payroll_ids = fields.One2many(
        comodel_name='operating.expense.report.payroll.rel',
        inverse_name='opr_exp_report_id',
        string='Total of Payroll',
    )
    payroll_amount = fields.Float('Payroll Amount')
    payroll_amount_a_year = fields.Float('Payroll Amount')
    payroll_amount_percent = fields.Float('Payroll Amount Percent')
    payroll_amount_percent_a_year = fields.Float('Payroll Amount')

    selling_exp_ids = fields.One2many(
        comodel_name='operating.expense.report.selling.rel',
        inverse_name='opr_exp_report_id',
        string='Total of Selling Expenses',
    )
    selling_amount = fields.Float('Payroll Amount')
    selling_amount_a_year = fields.Float('Payroll Amount')
    selling_amount_percent = fields.Float('Payroll Amount Percent')
    selling_amount_percent_a_year = fields.Float('Payroll Amount')

    administrative_exp_ids = fields.One2many(
        comodel_name='operating.expense.report.administrative.rel',
        inverse_name='opr_exp_report_id',
        string='Total of Administrative Expenses',
    )
    administrative_amount = fields.Float('Payroll Amount')
    administrative_amount_a_year = fields.Float('Payroll Amount')
    administrative_amount_percent = fields.Float('Payroll Amount Percent')
    administrative_amount_percent_a_year = fields.Float(
        'Payroll Amount Percent')

    def action_submit(self):
        # get report setting
        report_config = self.env['operating.expense.report.config'].search([
        ], limit=1)

        # get one year
        current_year = datetime(self.date_from.year, self.env.user.company_id.fiscalyear_last_month,
                                self.env.user.company_id.fiscalyear_last_day, 0, 0, 0)
        delta = relativedelta(months=12)
        satu_tahun_lalu = current_year - delta
        first_date_of_this_year = datetime(self.date_from.year, 1, 1, 0, 0, 0) # diganti ini untuk satu tahun ini

        # get net sales
        self.net_sales_account_id = report_config.net_sales_account_id.id

        sales_amount_aml = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', 'in', report_config.sales_account_ids.ids),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
             ])
        sales_amount = sum(sales_amount_aml.mapped('credit'))
        
        sales_return_amount_aml = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', 'in', report_config.sales_return_ids.ids),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
             ])
        sales_return_amount = sum(sales_return_amount_aml.mapped('debit'))

        self.net_sales_amount = sales_amount - sales_return_amount
        # net_sl_amt = self.env['account.move.line'].search(
        #     ['&', '&',
        #         ('account_id', '=', self.net_sales_account_id.id),
        #         ('date', '>=', self.date_from),
        #         ('date', '<=', self.date_to)
        #      ])
        # self.net_sales_amount = sum(net_sl_amt.mapped(
        #     'debit')) - sum(net_sl_amt.mapped('credit'))
        # self.net_sales_amount_a_year = sum(net_sl_amt_a_year.mapped(
        #     'debit')) - sum(net_sl_amt_a_year.mapped('credit'))

        sales_amount_a_year_aml = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', 'in', report_config.sales_account_ids.ids),
                ('date', '>', first_date_of_this_year),
                ('date', '<=', self.date_to)
             ])
        sales_amount_a_year = sum(sales_amount_a_year_aml.mapped('credit'))

        sales_return_amount_a_year_aml = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', 'in', report_config.sales_return_ids.ids),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
             ])
        sales_return_amount_a_year = sum(sales_return_amount_a_year_aml.mapped('debit'))
    

        self.net_sales_amount_a_year = sales_amount_a_year - sales_return_amount_a_year

        # ********************************************
        # # Get Payroll Expenses
        # ********************************************
        pay_exp_ids = []
        for acc in report_config.payroll_ids:

            # get account move line from this account
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date', '>=', self.date_from),
                 ('date', '<=', self.date_to)
                 ])
            # get amount from those account move lines
            acc_amount = sum(acc_amls.mapped('debit')) - \
                sum(acc_amls.mapped('credit'))

            if self.net_sales_amount > 0:
                acc_percent = acc_amount / self.net_sales_amount * 100
            else:
                acc_percent = 0.0

            # get account move line from this account
            acc_amls_a_year = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date', '>', first_date_of_this_year),
                 ('date', '<=', current_year)
                 ])
            # get amount from those account move lines
            acc_amount_a_year = sum(acc_amls_a_year.mapped('debit')) - \
                sum(acc_amls_a_year.mapped('credit'))

            if self.net_sales_amount_a_year > 0:
                acc_percent_a_year = acc_amount_a_year / self.net_sales_amount_a_year * 100
            else:
                acc_percent_a_year = 0.0

            pay_exp_ids.append((0, 0, {
                'account_id': acc.id,
                'account_value': acc_amount,
                'account_percent': acc_percent,
                'account_value_a_year': acc_amount_a_year,
                'account_percent_a_year': acc_percent_a_year,
            }))

        self.payroll_ids.unlink()
        self.payroll_ids = pay_exp_ids

        self.payroll_amount = sum(self.payroll_ids.mapped('account_value'))

        if self.net_sales_amount > 0:
            self.payroll_amount_percent = self.payroll_amount / self.net_sales_amount * 100
        else:
            self.payroll_amount_percent = 0.0

        self.payroll_amount_a_year = sum(
            self.payroll_ids.mapped('account_value_a_year'))

        if self.net_sales_amount_a_year > 0:
            self.payroll_amount_percent_a_year = self.payroll_amount_a_year / \
                self.net_sales_amount_a_year * 100
        else:
            self.payroll_amount_percent_a_year = 0.0
        
        # ********************************************
        # Get Selling Expenses
        # ********************************************
        sel_exp_ids = []
        for acc in report_config.selling_exp_ids:

            # get account move line from this account
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date', '>=', self.date_from),
                 ('date', '<=', self.date_to)
                 ])
            # get amount from those account move lines
            acc_amount = sum(acc_amls.mapped('debit')) - \
                sum(acc_amls.mapped('credit'))

            if self.net_sales_amount > 0:
                acc_percent = acc_amount / self.net_sales_amount * 100
            else:
                acc_percent = 0.0

            # get account move line from this account
            acc_amls_a_year = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date', '>', first_date_of_this_year),
                 ('date', '<=', current_year)
                 ])
            # get amount from those account move lines
            acc_amount_a_year = sum(acc_amls_a_year.mapped('debit')) - \
                sum(acc_amls_a_year.mapped('credit'))

            if self.net_sales_amount_a_year > 0:
                acc_percent_a_year = acc_amount_a_year / self.net_sales_amount_a_year * 100
            else:
                acc_percent_a_year = 0.0

            sel_exp_ids.append((0, 0, {
                'account_id': acc.id,
                'account_value': acc_amount,
                'account_percent': acc_percent,
                'account_value_a_year': acc_amount_a_year,
                'account_percent_a_year': acc_percent_a_year,
            }))

        self.selling_exp_ids.unlink()
        self.selling_exp_ids = sel_exp_ids

        self.selling_amount = sum(self.selling_exp_ids.mapped('account_value'))

        if self.net_sales_amount > 0:
            self.selling_amount_percent = self.selling_amount / self.net_sales_amount * 100
        else:
            self.selling_amount_percent = 0.0

        self.selling_amount_a_year = sum(
            self.selling_exp_ids.mapped('account_value_a_year'))

        if self.net_sales_amount_a_year > 0:
            self.selling_amount_percent_a_year = self.selling_amount_a_year / \
                self.net_sales_amount_a_year * 100
        else:
            self.selling_amount_percent_a_year = 0.0
    
        # ********************************************
        # # Get Administrative Expenses
        # ********************************************
        adm_exp_ids = []
        for acc in report_config.administrative_exp_ids:

            # get account move line from this account
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date', '>=', self.date_from),
                 ('date', '<=', self.date_to)
                 ])
            # get amount from those account move lines
            acc_amount = sum(acc_amls.mapped('debit')) - \
                sum(acc_amls.mapped('credit'))

            if self.net_sales_amount > 0:
                acc_percent = acc_amount / self.net_sales_amount * 100
            else:
                acc_percent = 0.0

            # get account move line from this account
            acc_amls_a_year = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date', '>', first_date_of_this_year),
                 ('date', '<=', current_year)
                 ])
            # get amount from those account move lines
            acc_amount_a_year = sum(acc_amls_a_year.mapped('debit')) - \
                sum(acc_amls_a_year.mapped('credit'))

            if self.net_sales_amount_a_year > 0:
                acc_percent_a_year = acc_amount_a_year / self.net_sales_amount_a_year * 100
            else:
                acc_percent_a_year = 0.0

            adm_exp_ids.append((0, 0, {
                'account_id': acc.id,
                'account_value': acc_amount,
                'account_percent': acc_percent,
                'account_value_a_year': acc_amount_a_year,
                'account_percent_a_year': acc_percent_a_year,
            }))

        self.administrative_exp_ids.unlink()
        self.administrative_exp_ids = adm_exp_ids

        self.administrative_amount = sum(self.administrative_exp_ids.mapped('account_value'))

        if self.net_sales_amount > 0:
            self.administrative_amount_percent = self.administrative_amount / self.net_sales_amount * 100
        else:
            self.administrative_amount_percent = 0.0

        self.administrative_amount_a_year = sum(
            self.administrative_exp_ids.mapped('account_value_a_year'))

        if self.net_sales_amount_a_year > 0:
            self.administrative_amount_percent_a_year = self.administrative_amount_a_year / \
                self.net_sales_amount_a_year * 100
        else:
            self.administrative_amount_percent_a_year = 0.0
        
        # generate report action
        return self.env.ref('sanwa_manufacturing_cost_report.operating_expenses_report_action').report_action(self)
