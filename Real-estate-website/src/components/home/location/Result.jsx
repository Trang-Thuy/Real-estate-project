import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import usePropertyDetails from "../../../usePropertyDetails";
import Heading from "../../common/Heading";
import HomeSearch from "../hero/Hero";
import RecentCard from "../recent/RecentCard";
import Detail from "../../services/Details";

const Result = ({ city: cityProp }) => {
  const { selectedProperty, showModal, handleMoreInfo, handleClose } = usePropertyDetails();
  const { city: cityParam } = useParams(); // Get city parameter from URL
  const [apartments, setApartments] = useState([]);

  useEffect(() => {
    const city = cityProp || cityParam;
    if (city) {
      axios
        .get(`http://localhost:5000/location/${city}`)
        .then((response) => {
          setApartments(response.data);
        })
        .catch((error) => {
          console.error("There was an error fetching the data!", error);
        });
    }
  }, [cityProp, cityParam]);

  return (
    <>
      <HomeSearch />
      <section className="recent padding">
        <div className="container">
          <Heading
            title={`Search Result for ${apartments[0]?.province || "Unknown"}`}
            subtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."
          />
          <RecentCard city={apartments} onMoreInfo={handleMoreInfo} />
          {showModal && selectedProperty && (
            <Detail property={selectedProperty} onClose={handleClose} />
          )}
        </div>
      </section>
    </>
  );
};

export default Result;
