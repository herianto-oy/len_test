# Dokumentasi API Time Off

## Versi API
v1.0.0

## Gambaran Umum

API ini memungkinkan Anda untuk mengelola permintaan cuti (time off) dalam sistem Odoo 18. Anda dapat melihat, menyetujui, menolak, atau mereset status permintaan cuti melalui permintaan HTTP.

## Persyaratan

- Odoo 18.x sudah terinstal.

## Instalasi Modul Secara Manual

- Salin modul `len_leave_request` ke direktori `addons_customn` di instalasi Odoo. 
- Restart Service odoo  `sudo service odoo restart`.
- Login sebagi superuser lalu `Update Apps List`.
- Active / instal modul `len_leave_request`.
   
# REST API
## 1. POST /api/time_off

### Request Format

**Method**: `POST`  
**URL**: `/api/time_off`  
**Content-Type**: `application/json`

### Request Body

```json
{
    "id": "integer",
    "status": "string"
}
```

### Response Body
```json
{
    "status": "string",
    "code": "integer",
    "data": {
        "status": "string",
        "message": "string"
    }
}

```

### Deskripsi
Endpoint ini digunakan untuk memperbarui status dari permintaan cuti tertentu berdasarkan ID dan status yang diberikan.

1. id (wajib): ID dari permintaan cuti yang ingin Anda perbarui.
2. status (wajib): Status baru untuk permintaan cuti. Nilai yang dapat dipilih:
- "validate": Menyetujui permintaan cuti.
- "refuse": Menolak permintaan cuti.
- "reset": Mereset permintaan cuti ke status awal.


### Contoh Request Body
```json
{
    "id": 1,
    "status": "validate"
}
```

### Contoh Response Body Berhasil
```json
{
    "status": "Success",
    "code": 200,
    "data": {
        "id": 1,
        "status": "Success",
        "message": "Status has been updated to validate"
    }
}

```
### Contoh Response Body Error 1
```json
{
    "status": "Success",
    "code": 200,
    "data": {
        "id": 1,
        "status": "Error",
        "message": "Time off request state must be Refused or Cancelled in order to be reset to Confirmed."
    }
}
```

### Contoh Response Body Error 2
```json
{
    "status": "Failed Invalid Time Off Id",
    "code": 200,
    "data": null
}
```

## 2. GET /api/time_off

### Request Format

**Method**: `POST`  
**URL**: `/api/time_off`  
**Content-Type**: `application/json`
- id (opsional): ID permintaan cuti spesifik yang ingin diambil.

### Response Body
```json
{
  "code": "integer",
  "status": "string",
  "message": "string",
  "data": [
    {
      "id": "integer",
      "employee_id": "integer",
      "employee_name": "string",
      "request_date_from": "string",
      "request_date_to": "string",
      "number_of_days": "float",
      "status": "string"
    }
  ]
}
```

### Contoh Request
GET /api/time_off

### Contoh Response
```json
{
    "code": 200,
    "status": "Success",
    "message": "Data found",
    "data": [
        {
            "id": 12,
            "employee_id": 18,
            "employee_name": "Paul Williams",
            "request_date_from": "2025-03-05 00:00:00",
            "request_date_to": "2025-03-05 00:00:00",
            "number_of_days": 1.0,
            "status": "validate"
        },
        {
            "id": 10,
            "employee_id": 15,
            "employee_name": "Sharlene Rhodes",
            "request_date_from": "2024-11-25 00:00:00",
            "request_date_to": "2024-11-27 00:00:00",
            "number_of_days": 3.0,
            "status": "refuse"
        },
        {
            "id": 2,
            "employee_id": 1,
            "employee_name": "Mitchell Admin",
            "request_date_from": "2024-11-25 00:00:00",
            "request_date_to": "2024-11-27 00:00:00",
            "number_of_days": 3.0,
            "status": "validate"
        }
    ]
}
```

### Contoh Request
GET /api/time_off?id=1

### Contoh Response Berhasil
```json
{
    "code": 200,
    "status": "Success",
    "message": "Success",
    "data": [
        {
            "id": 1,
            "employee_id": 1,
            "employee_name": "Mitchell Admin",
            "request_date_from": "2024-11-04 00:00:00",
            "request_date_to": "2024-11-06 00:00:00",
            "number_of_days": 3.0,
            "status": "validate"
        }
    ]
}
```

### Contoh Response Gagal
```json
{
    "code": 200,
    "status": "Failed",
    "message": "Invalid id Time Off",
    "data": []
}
```
