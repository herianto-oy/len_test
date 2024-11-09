# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.wrappers import Response
from odoo.exceptions import UserError
import json

class LeaveRequestController(http.Controller):
    @http.route('/api/time_off', type='http', auth='public', methods=['POST'], csrf=False)
    def post_time_off(self, **params):
        request_data = request.httprequest.get_json()
        time_off_id = request_data.get('id')
        time_off = request.env['hr.leave'].sudo().search([('id', '=', int(time_off_id))])
        if time_off_id and time_off:
            status = request_data.get('status')
            data = {'id' : time_off_id}
            try:
                if status == 'validate':
                    time_off.action_approve()
                    data['status'] = 'Success'
                    data['message'] = 'Status has been updated to validate'
                elif status == 'refuse':
                    time_off.action_refuse()
                    data['status'] = 'Success'
                    data['message'] = 'Status has been updated to refuse'
                else:
                    time_off.action_reset_confirm()
                    data['status'] = 'Reseted'
            except UserError as e:
                data['status'] = 'Error'
                data['message'] = str(e).replace('"', '')

            return Response(
                content_type='application/json; charset=utf-8',
                response=json.dumps({
                    "status": "Success", 
                    "code": 200,
                    "data": data
                }),
                status=200
            )
        else:
            return Response(
                content_type='application/json; charset=utf-8',
                response=json.dumps({
                    "status": "Failed Invalid Time Off Id", 
                    "code": 200,
                    "data": None
                }),
                status=200
            )
    
    @http.route('/api/time_off', type='http', auth='public', methods=['GET'], csrf=False)
    def get_time_off(self, **params):
        time_off_id = params.get('id')
        if not time_off_id:
            time_off_records = request.env['hr.leave'].sudo().search([])
            data = []
            for time_off in time_off_records:
                data.append({
                    "id": time_off.id,
                    "employee_id": time_off.employee_id.id,
                    "employee_name": time_off.employee_id.name,
                    "request_date_from": time_off.request_date_from.strftime('%Y-%m-%d %H:%M:%S') if time_off.request_date_from else None,
                    "request_date_to": time_off.request_date_to.strftime('%Y-%m-%d %H:%M:%S') if time_off.request_date_to else None,
                    "number_of_days": time_off.number_of_days,
                    "status": time_off.state,
                })
            return Response(
                content_type='application/json; charset=utf-8',
                response=json.dumps({
                    "code": 200,
                    "status": "Success", 
                    "message": "Data found" if len(data) > 0 else "Data not found",
                    "data": data
                }),
                status=200
            )
        else:
            time_off = request.env['hr.leave'].sudo().search([('id', '=', int(time_off_id))])
            data = []
            if time_off:
                data.append({
                    "id": time_off.id,
                    "employee_id": time_off.employee_id.id,
                    "employee_name": time_off.employee_id.name,
                    "request_date_from": time_off.request_date_from.strftime('%Y-%m-%d %H:%M:%S') if time_off.request_date_from else None,
                    "request_date_to": time_off.request_date_to.strftime('%Y-%m-%d %H:%M:%S') if time_off.request_date_to else None,
                    "number_of_days": time_off.number_of_days,
                    "status": time_off.state,
                })

            
                return Response(
                    content_type='application/json; charset=utf-8',
                    response=json.dumps({
                        "code": 200,
                        "status": "Success",
                        "message": "Success",
                        "data": data
                    }),
                    status=200
                )
            else:
                return Response(
                    content_type='application/json; charset=utf-8',
                    response=json.dumps({
                        "code": 200,
                        "status": "Failed", 
                        "message": "Invalid id Time Off",
                        "data": data
                    }),
                    status=200
                )
