import { Button } from '@material-ui/core'
import {
  Grid,
  makeStyles,
  TextField,
  FormControl,
  FormLabel,
  RadioGroup,
  Radio,
  FormControlLabel,
} from '@material-ui/core'
import React from 'react'
import { useState } from 'react'
import { useMutation } from 'react-query'
import { addPatient, updatePatient, PatientType } from '../requests/api'

const useStyles = makeStyles(theme => ({
  root: { '& .MuiFormControl-root': { width: '80%', margin: theme.spacing(1) } },
}))

const initialValues = {
  name: '',
  sex: 'male',
  age: '',
  identity_number: '',
  municipality: 'Holguin',
  province: 'Holguin',
}
export type AddEditFormType = {
  state: string
  patient?: PatientType
}

export const AddEditForm = ({ state, patient }: AddEditFormType) => {
  const classes = useStyles()
  const [values, setValues] = useState(patient || initialValues)
  console.log(values)
  const addPatientMutation = useMutation(addPatient)
  const updatePatientMutation = useMutation(updatePatient)
  console.log(patient)
  const hanldeInputChange = (e: any) => {
    console.log(e.target)
    setValues({ ...values, [e.target.name]: e.target.value })
  }

  return (
    <form className={classes.root}>
      <Grid container>
        <Grid item xs={6}>
          <TextField
            id="outlined-basic"
            label="Nombre y Apellidos"
            variant="outlined"
            name="name"
            value={values.name}
            onChange={hanldeInputChange}
          />
          <TextField
            id="outlined-basic"
            label="Provincia"
            variant="outlined"
            name="province"
            value={values.province}
            onChange={hanldeInputChange}
          />
          <TextField
            id="outlined-basic"
            label="Municipio"
            variant="outlined"
            name="municipality"
            value={values.municipality}
            onChange={hanldeInputChange}
          />
        </Grid>
        <Grid item xs={6}>
          <FormControl component="fieldset">
            <FormLabel component="legend">Gender</FormLabel>
            <RadioGroup row aria-label="genero" name="sex" value={values.sex} onChange={hanldeInputChange}>
              <FormControlLabel value="female" control={<Radio />} label="Femenino" />
              <FormControlLabel value="male" control={<Radio />} label="Masculino" />
              <FormControlLabel value="other" control={<Radio />} label="Otro" />
            </RadioGroup>
          </FormControl>
          <TextField
            id="outlined-basic"
            label="CID"
            variant="outlined"
            name="identity_number"
            value={values.identity_number}
            onChange={hanldeInputChange}
          />
          <TextField
            id="outlined-basic"
            label="Edad"
            variant="outlined"
            name="age"
            value={values.age}
            onChange={hanldeInputChange}
          />
          <Button
            variant="outlined"
            onClick={() => (state == 'edit' ? updatePatientMutation.mutate(values) : addPatientMutation.mutate(values))}
          >
            {state == 'edit' ? 'Editar' : 'Aceptar'}
          </Button>
        </Grid>
      </Grid>
    </form>
  )
}
