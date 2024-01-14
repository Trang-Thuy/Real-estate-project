import React from "react"
import Heading from "../../common/Heading"
import "./Featured.css"
import FeaturedCard from "./FeaturedCard"

const Featured = () => {
  return (
    <>
      <section className='featured background'>
        <div className='container'>
          <Heading title='What do we have' subtitle='We can bring to you many choice of apartment and saler' />
          <FeaturedCard />
        </div>
      </section>
    </>
  )
}

export default Featured
