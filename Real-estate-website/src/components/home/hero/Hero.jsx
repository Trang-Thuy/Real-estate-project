import React from "react"
import Heading from "../../common/Heading"
import "./hero.css"

const Hero = () => {
  return (
    <>
      <section className='hero'>
        <div className='container'>
          <Heading title='Search Your Next Apartment ' subtitle='Find new & featured property located in your local city.' />
          

          <form className='flex'>
            <div className='box'>
              <span>City/Street</span>
              <select>
                <option value = ''>Select City/Province</option>
                <option value = 'city1'>Ha Noi</option>
                <option value = 'city2'>Ho Chi Minh</option>
                <option value = 'city3'>Vung Tau</option>

              </select>
              {/* <input type='text' placeholder='Location' /> */}
              
            </div>
            {/* <div className='box'>
              <span>Project Name</span>
              <input type='text' placeholder='Property Type' />
            </div> */}
            <div className='box'>
              <span>District</span>
              {/* <input type='text' placeholder='Price Range' /> */}
              <select>
                <option value = ''>All</option>
                <option value = 'city1'>Ha Noi</option>
                <option value = 'city2'>Ho Chi Minh</option>
                <option value = 'city3'>Vung Tau</option>

              </select>
            </div>
            {/* <div className='box'>
              <span>Ward</span>
              <input type='text' placeholder='Price Range' />
            </div> */}
            <div className='box'>
              <span>Price Range (unit: Milions)</span>
              {/* <input type='text' placeholder='Price Range' /> */}
              <select>
                <option value = ''>All Range</option>
                <option value = 'city1'>0 - 500</option>
                <option value = 'city2'>500 - 2000</option>
                <option value = 'city3'>2000 - </option>

              </select>
            </div>
            {/* <div className='box'>
              <h4>Advance Filter</h4>
            </div> */}
            <button className='btn1'>
              <i className='fa fa-search'></i>
            </button>
          </form>
          
        </div>
      </section>
    </>
  )
}

export default Hero
