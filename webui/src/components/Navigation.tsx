/* eslint-disable @typescript-eslint/no-non-null-asserted-optional-chain */
/* eslint-disable @typescript-eslint/no-non-null-assertion */
import { List, ListItem } from '@material-ui/core'
import { Fab } from '@material-ui/core'
import { AppBar, Avatar, Divider, Drawer, makeStyles, Toolbar, Typography, IconButton } from '@material-ui/core'
import DeleteIcon from '@material-ui/icons/Delete'
import EditIcon from '@material-ui/icons/Edit'
import React, { useState } from 'react'
import { useMutation, useQueryClient } from 'react-query'
import AddIcon from '@material-ui/icons/Add'

import { useFetchPatients } from '../hooks'
import { deletePatient } from '../requests/api'
import { Popup } from './Popup'
import { AddEditForm } from './AddEditForm'

const drawerWidth = 240

export type PatientType = {
  id?: number
  name: string
  sex: string
  age: string
  identity_number: string
  municipality: string
  province: string
}

const useStyles = makeStyles(theme => ({
  appBar: {
    width: `calc(100% - ${drawerWidth}px)`,
  },
  drawer: {
    width: drawerWidth,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  small: {
    width: theme.spacing(4),
    height: theme.spacing(4),
  },
  fab: {
    position: 'absolute',
    bottom: theme.spacing(2),
    right: theme.spacing(2),
  },
}))

export const Navigation = () => {
  const classes = useStyles()
  const { isLoading, error, data, refetch } = useFetchPatients()
  const [state, setState] = useState('add')
  const [currentPatient, setCurrentPatient] = useState({
    name: '',
    sex: '',
    age: '',
    identity_number: '',
    municipality: '',
    province: '',
  })
  const deletePatientMutation = useMutation(deletePatient, { onSuccess: () => refetch() })
  const [openPopup, setOpenPopup] = useState(false)

  return (
    <>
      <AppBar className={classes.appBar} elevation={0}>
        <Toolbar>
          <Typography style={{ flexGrow: 1 }}>MRI Segmentation Demo 1</Typography>
          <Typography style={{ marginRight: 10 }}>Dr. Jhon Doe</Typography>
          <Avatar src="./logo-doctor.png" />
        </Toolbar>
      </AppBar>
      <Drawer className={classes.drawer} variant="permanent" anchor="left" classes={{ paper: classes.drawerPaper }}>
        <Typography variant="h5" style={{ margin: 30, justifyContent: 'center', alignItems: 'center' }}>
          Pacientes
        </Typography>
        <Divider></Divider>
        <div
          style={{
            display: 'flex',
            flexDirection: 'row',
            flexBasis: 'inline',
            marginLeft: 30,
            marginTop: 30,
          }}
        >
          {!isLoading && (
            <List>
              {data.map((patient: PatientType) => (
                <>
                  <ListItem
                    key={patient?.id}
                    style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', marginBottom: 4 }}
                  >
                    <Typography gutterBottom>{patient?.name}</Typography>
                    <div style={{ display: 'flex', flexDirection: 'row' }}>
                      <IconButton
                        aria-label="edit"
                        style={{ marginRight: 1 }}
                        onClick={() => {
                          setState('edit'), setCurrentPatient(patient), setOpenPopup(true)
                        }}
                      >
                        <EditIcon fontSize="small" />
                      </IconButton>
                      <IconButton
                        aria-label="delete"
                        color="secondary"
                        onClick={() => {
                          deletePatientMutation.mutate(patient?.id!)
                        }}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </div>
                  </ListItem>
                  <Divider style={{ marginLeft: 10, marginRight: 30 }} />
                </>
              ))}
            </List>
          )}
        </div>
      </Drawer>
      <Fab
        color="primary"
        aria-label="add"
        className={classes.fab}
        onClick={() => {
          setState('add'), setOpenPopup(true)
        }}
      >
        <AddIcon />
      </Fab>
      <Popup title="Añadir Paciente" openPopup={openPopup} setOpenPopup={setOpenPopup}>
        {state === 'edit' ? <AddEditForm state={state} patient={currentPatient} /> : <AddEditForm state={state} />}
      </Popup>
    </>
  )
}
