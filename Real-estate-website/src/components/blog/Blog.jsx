import React from "react"
import Back from "../common/Back"
import RecentCard from "../home/recent/RecentCard"
import "../home/recent/recent.css"
import "../Agent/about.css"
import img from "../images/about.jpg"

const Blog = () => {
  return (
    <>
      <section className='blog-out mb'>
        <Back name='Dự đoán giá' title='Dự đoán giá nhà theo thông tin bạn cung cấp' cover={img} />
        <div className='container recent'>
        <form className='flex'>
        <h4>Fillup The Form</h4> <br />
            <div className='box'>
            
              <span>City/Province</span>
              <select>
                {/* <option value = ''>Select City/Province</option> */}
                <option value = 'city1'>Name</option>
                <option value = 'city2'>Email</option>
                <option value = 'city3'>Phone number</option>

              </select>

              
            </div>
            <div className='box'>
            
              <span>District</span>
              <select>
                {/* <option value = ''>Select City/Province</option> */}
                <option value = 'city1'>Ha Dong</option>
                <option value = 'city2'>Dong Tam</option>
                <option value = 'city3'>Quan 1</option>

              </select>

              
            </div>
            <div className='box'>
            
              <span>Square range</span>
              <select>
                {/* <option value = ''>Select City/Province</option> */}
                <option value = 'city1'>0 - 100</option>
                <option value = 'city2'>100-500</option>
                <option value = 'city3'>500-</option>

              </select>

              
            </div>
            {/* <div className='box'>
              <span>Enter information here</span>
              <input type='text' placeholder='Enter information here' />
            </div> */}
            <button className='btn2'>Search</button>
            {/* <input type = "submit" value = "Submit"></input> */}
          </form>
          <h4>Có thể bạn quan tâm</h4> <br />
          <RecentCard />
        </div>
        
        
      </section>
    </>
  )
}

export default Blog
