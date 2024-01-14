import React from "react"
import Back from "../common/Back"
import Heading from "../common/Heading"
import img from "../images/about.jpg"
import "./about.css"
// import Team from "./team/Team"
import Team from "../home/team/Team"
import "../home/team/team.css"


const Agent = () => {
  return (
    <>
      <section className='about'>
        <Back name='Agent Chart' title='Authority of Agent Chart' cover={img} class = "back_img"/>
        <div className='container flex mtop'>
          <div className='left row'>
            <Heading title='Xep hang do tin cay cua agent' subtitle='Check out our company story and work process' />

            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.</p>
            
            <form className='flex'>
            <div className='box'>
              <span>Search by name/email/phone number</span>
              <select>
                {/* <option value = ''>Select City/Province</option> */}
                <option value = 'city1'>Name</option>
                <option value = 'city2'>Email</option>
                <option value = 'city3'>Phone number</option>

              </select>
              
            </div>
            <div className='box'>
              <span>Enter information here</span>
              <input type='text' placeholder='Enter information here' />
            </div>
            <button className='btn2'>Search</button>
            {/* <input type = "submit" value = "Submit"></input> */}
          </form>
          
          
          </div>
          <div className='right row'>
            <img src='./immio.jpg' alt='' />
          </div>
        </div>
      </section>
      <Team></Team>
    </>
  )
}

export default Agent
