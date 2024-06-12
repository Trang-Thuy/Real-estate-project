import { useState } from 'react';
import axios from 'axios';

const usePropertyDetails = () => {
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const handleMoreInfo = async (id) => {
    try {
      const response = await axios.get(`http://localhost:5000/moreinfo/${id}`);
      setSelectedProperty(response.data);
      setShowModal(true);
    } catch (error) {
      console.error("There was an error fetching the detail data!", error);
    }
  };

  const handleClose = () => {
    setShowModal(false);
    setSelectedProperty(null);
  };

  return { selectedProperty, showModal, handleMoreInfo, handleClose };
};

export default usePropertyDetails;
