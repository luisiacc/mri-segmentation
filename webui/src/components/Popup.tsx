/* eslint-disable react/prop-types */
/* eslint-disable @typescript-eslint/no-unused-vars */
import React from 'react'
import { Dialog, DialogTitle, DialogContent } from '@material-ui/core'

export type PopupProps = {
  title: string
  children: React.ReactNode
  openPopup: boolean
  setOpenPopup: React.Dispatch<React.SetStateAction<boolean>>
}

export const Popup = ({ title, children, openPopup, setOpenPopup }: PopupProps) => {
  const handleClose = () => setOpenPopup(false)
  return (
    <Dialog open={openPopup} onClose={handleClose} maxWidth="md">
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>{children}</DialogContent>
    </Dialog>
  )
}
