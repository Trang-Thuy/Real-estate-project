import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import "./Services.css";

const Detail = ({property, onClose}) => {
  if (!property) return null;

  const {title, category, address, price, square, source, img_url, name, number_bedroom, number_wc, contact_name, contact_phone, url, description, legal} = property;

  let img_array = [];
  try {
    img_array = img_url.substring(1, img_url.length - 1).split(',').map(item => item.replace(/'/g, ''));
  } catch (error) {
    console.error('Error parsing img_url:', error);
  }
  category = "Authorized"

  
  return (
    <>
      <div className="overlay1">
        <div className="detail-modal">
          <section className="services">
            <section className="service">
            <button className="close-btn" onClick={onClose}>X</button>
              <div className="box shadow flex">
              <div className="title">{title}</div>
                <div className="img">
                  {img_array.map((img, index) => (
                    <img key={index} src={img} alt={name} />
                  ))}
                </div>
                <hr></hr>
                <div className="text">
                  
                  <div className="category flex">
                    <span
                      style={{
                        background: category === "Authorized" ? "#25b5791a" : "#ff98001a",
                        color: category === "Authorized" ? "#25b579" : "#ff9800",
                      }}
                    >
                      {category}
                    </span>
                    
                    <i className="fa fa-bookmark"></i>
                  </div>
                  <h4>{name}</h4>
                  <div className="category flex">
                    <p>
                      <i className="fa fa-location-dot"></i> {address}
                    </p>
                    <p>
                      <i className="fa fa-credit-card"></i> {price}
                    </p>
                    <p>
                      <i className="fa fa-square"></i> {square}
                    </p>
                  </div>
                  <h4>Facibility</h4>
                  <div className="flex">
                    <p>
                      <i className="fa fa-location-dot"></i> {number_bedroom} bedroom
                    </p>
                    <p>
                      <i className="fa fa-location-dot"></i> {number_wc}wc
                    </p>
                    <p>
                      <i className="fa fa-location-dot"></i> {legal}
                    </p>
                    <p>
                      <i className="fa fa-location-dot"></i> co may giat
                    </p>
                  </div>
                  <h4>Mo ta chi tiet</h4>
                  <p>{description}</p>
                  <h4>Thong tin lien he</h4>
                  <table>
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Phone Number</th>
                        <th>Source</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>{contact_name}</td>
                        <td>0{contact_phone}</td>
                        <td><a href={url}>{source}</a></td>
                      </tr>
                      <tr>
                        <td>Nguyen Mai Phuong</td>
                        <td>09879375843</td>
                        <td>mogi.vn</td>
                      </tr>
                      <tr>
                        <td>Nguyen Mai Phuong</td>
                        <td>09879375843</td>
                        <td>mogi.vn</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
          </section>
        </div>
      </div>
    </>
  );
};

export default Detail;
