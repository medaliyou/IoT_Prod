import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { Form, Button, Container, Alert } from 'react-bootstrap';
import AuthService, { SD_API } from "../../services/auth.service"

const AddSD = () => {
  
  const user = AuthService.getCurrentUser()

  const navigate = useNavigate();
  const [enteredTag, setTag] = useState('');

  React.useEffect(() => {

    if (null === user) {
      navigate("/", { replace: true });
    }
  }, [])


  const tagChangeHandler = (event) => {
    setTag(event.target.value);
  };


  const submitActionHandler = (event) => {
    event.preventDefault();
    SD_API
      .post("SD/", {
        TAG_SD: enteredTag,
      })
      .then((response) => {
        console.log(response)
        alert("Smart Device " + enteredTag + " added!");
        navigate("/SD");
      }).catch(error => {
        if (error.response.status === 409) {
          alert("Smart Device with " + enteredTag + " exists");

        } else {
          console.log(error)
          alert("error===" + error);

        }
      });

  };


  const cancelHandler = () => {
    //reset the values of input fields
    setTag('');
    navigate("/SD");

  }
  return (
    <div>
      <Alert variant='primary'>
        <Container>
          <Form onSubmit={submitActionHandler}>
            <Form.Group controlId="form.Tag">
              <Form.Label>Smart Device Tag</Form.Label>
              <Form.Control type="text" value={enteredTag} onChange={tagChangeHandler} placeholder="Enter Smart Device Tag" required />
            </Form.Group>
            <br></br>
            <Button type='submit'>Add SD</Button>
            &nbsp;&nbsp;&nbsp;
            <Button type='submit' onClick={() => cancelHandler()}>Cancel</Button>
          </Form>

        </Container>
      </Alert>
    </div>
  );
}
export default AddSD;
