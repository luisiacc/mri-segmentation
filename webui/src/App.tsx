import { Button } from '@material-ui/core'
import React from 'react'
import { Navigation } from './components'
import { QueryClient } from 'react-query'

import { useFetchPatients, useFetchMRI } from './hooks'

export type PatientType = {
  id?: number
  name: string
  sex: string
  age: number
  identity_number: string
  municipality: string
  province: string
}

export type MRIsParams = {
  file: File
  patient: PatientType
}

const queryClient = new QueryClient()

const App = () => {
  return <Navigation />
}

function ExamplePatientApi() {
  const { isLoading, error, data } = useFetchPatients()
  console.log('patients', data)

  if (isLoading) return <p>Loading... </p>

  if (error) return <p>{'An error has occurred: ' + error.message}</p>

  return data.map((patient: PatientType) => (
    <div key={patient?.id}>
      <h1>{patient?.name}</h1>
      <p>{patient?.sex}</p>
      <p>{patient?.age}</p>
      <p>{patient?.identity_number}</p>
      <p>{patient?.municipality}</p>
      <p>{patient?.province}</p>
    </div>
  ))
}

function ExampleMRIsApi() {
  const { isLoading, error, data, refetch } = useFetchMRI('1')
  console.log('mris', data)

  if (isLoading) return <p>Loading... </p>

  if (error) return <p>{'An error has occurred: ' + error.message}</p>

  return (
    <Button variant="contained" component="label" onClick={() => refetch()}>
      Upload File
      {/*  <input type="file" hidden /> */}
    </Button>
  )
}

export default App
