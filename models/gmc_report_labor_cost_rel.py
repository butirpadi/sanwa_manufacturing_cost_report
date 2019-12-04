from odoo import api, fields, models


class GmcReportLaborCostRel(models.TransientModel):
    _name = 'gmc.report.labor.cost.rel'
    _description = 'Relation of gmc report with labor cost'

    gmc_report_id = fields.Many2one(
        'gmc.report', string='GMC Report', ondelete='cascade',)
    account_id = fields.Many2one(
        'account.account', string="Account", ondelete='cascade',)
    account_value = fields.Float('Account Value')
