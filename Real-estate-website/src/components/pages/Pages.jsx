import React from "react"
import Header from "../common/header/Header"
import Footer from "../common/footer/Footer"
import { Outlet } from 'react-router-dom';

const Pages = () => {
  return (
    <>
        <Header />
        <Outlet />
        <Footer />
    </>
  )
}

export default Pages
