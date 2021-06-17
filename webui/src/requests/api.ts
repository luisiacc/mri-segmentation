import axios from 'axios'

import { API_URL } from '../utils/constants'

export type PatientType = {
  id?: number
  name: string
  sex: string
  age: string
  identity_number: string
  municipality: string
  province: string
}

//CRUD Patients
export const getPatients = () => axios.get(`${API_URL}/patients`)

export const addPatient = (patient: PatientType) => axios.post(`${API_URL}/patients/`, { params: { patient } })

export const updatePatient = (patient: PatientType) =>
  axios.put(`${API_URL}/patients/${patient.id}`, { params: { patient } })

export const deletePatient = (patient: number) => axios.delete(`${API_URL}/patients/${patient}`)

//CRUD MRI
export const getMRI = (patient: string) => axios.get(`${API_URL}/mris/`, { params: { patient } })

export const addMRI = (mrisParams: any) => axios.post(`${API_URL}/mris`, mrisParams)

export const updateMRI = (patient: string) => axios.patch(`${API_URL}/mris/`, { params: { patient } })

export const deleteMRI = (mriID: string) => axios.delete(`${API_URL}/mris/`, { params: { mriID } })
