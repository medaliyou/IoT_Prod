import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { MU_API } from "../../services/auth.service"

const Register = () => {

  const navigate = useNavigate();
  const param = useParams();
  const [tag, setTag] = useState('');
  const [id, setId] = useState('');
  const [pw, setPassword] = useState('');

  useEffect(() => {
  }, []);

  const tagChangeHandler = (event) => {
    setTag(event.target.value);
  };

  const idChangeHandler = (event) => {
    setId(event.target.value);
  };

  const passwordChangeHandler = (event) => {
    setPassword(event.target.value);
  };


  const submitActionHandler = (event) => {
    event.preventDefault();
    MU_API
      .post("MU/", {
        TAG: tag,
        ID: id,
        PW: pw
      })
      .then((response) => {
        alert("MU " + tag + " registered!");
        navigate('/')

      }).catch(error => {
        alert("Error Ocurred registering MU:" + error);
      });

  };

  return (
    <Alert variant='primary'>
      <Container>
        <Form onSubmit={submitActionHandler} id="data">
          <Form.Group controlId="form.id">
            <Form.Label>Tag</Form.Label>
            <Form.Control type="text" value={tag} onChange={tagChangeHandler} placeholder="Enter Tag" required />
          </Form.Group>
          <Form.Group controlId="form.Name">
            <Form.Label>Id</Form.Label>
            <Form.Control type="text" value={id} onChange={idChangeHandler} placeholder="Enter User Name" required />
          </Form.Group>
          <Form.Group controlId="form.Role">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" value={pw} onChange={passwordChangeHandler} placeholder="Enter Password" required />
          </Form.Group>
          <br></br>
          <Button type='submit'>Register</Button>
          &nbsp;&nbsp;&nbsp;
          <Button type='submit' onClick={() => navigate("/")}>Cancel</Button>
        </Form>
      </Container>
    </Alert>

  );
}
export default Register;