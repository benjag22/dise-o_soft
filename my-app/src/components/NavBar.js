import React from 'react'
import './NavBar.css'
import logo from './assets/logo.png'

export function NavBar() {
  return (
    <nav >
        <a href='/' id='boton_home'><img src={logo} width="55"/></a>
    </nav>
  )
}

