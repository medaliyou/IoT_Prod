import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

import Register from "./MU/Register";
import Login from './MU/Login';

import AuthService, { MU_API, SD_API } from "../services/auth.service"
import { Form, Button, Container, Alert } from 'react-bootstrap';


const Home = () => {

  const user = AuthService.getCurrentUser()

  const navigate = useNavigate();
  const param = useParams();
  const [id, setId] = useState('');
  const [pw_old, setPasswordOld] = useState('');
  const [pw_new, setPasswordNew] = useState('');

  useEffect(() => {
  }, []);



  const idChangeHandler = (event) => {
    setId(event.target.value);
  };

  const passwordOldChangeHandler = (event) => {
    setPasswordOld(event.target.value);
  };
  const passwordNewChangeHandler = (event) => {
    setPasswordNew(event.target.value);
  };

  const logOut = () => {
    AuthService.MU_API.post("app/v1/logout").then((response) => {
      alert("MU logged out!");
      localStorage.removeItem("user");
      
      window.location.reload();


    }).catch(error => {
      alert("Error Ocurred Logging out MU:" + error);
    });

  };


  const submitActionHandler = (event) => {
    event.preventDefault();
    MU_API
      .post("app/v1/update_password", {
        ID: id,
        PW_old: pw_old,
        PW_new: pw_new
      })
      .then((response) => {
        alert("MU " + id + " password updated!");
        logOut()
        navigate('/MU/Login')

      }).catch(error => {
        alert("Error Ocurred registering MU:" + error);
      });

  };

  return (
    <div>
      {user && (
        <Alert variant='primary'>
          <Container>
            <Form onSubmit={submitActionHandler} id="data">
              <Form.Group controlId="form.Name">
                <Form.Label>Id</Form.Label>
                <Form.Control type="text" value={id} onChange={idChangeHandler} placeholder="Enter User Name" required />
              </Form.Group>
              <Form.Group controlId="form.PasswordOld">
                <Form.Label>Old Password</Form.Label>
                <Form.Control type="password" value={pw_old} onChange={passwordOldChangeHandler} placeholder="Enter Old Password" required />
              </Form.Group>
              <Form.Group controlId="form.PasswordNew">
                <Form.Label>New Password</Form.Label>
                <Form.Control type="password" value={pw_new} onChange={passwordNewChangeHandler} placeholder="Enter New Password " required />
              </Form.Group>
              <br></br>
              <Button type='submit'>Update Password</Button>
              &nbsp;&nbsp;&nbsp;
              <Button type='submit' onClick={() => navigate("/")}>Cancel</Button>
            </Form>
          </Container>
        </Alert>
      )}
    </div>
  )
};

export default Home;