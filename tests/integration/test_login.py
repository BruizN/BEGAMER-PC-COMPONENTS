async def test_login_success(client, test_user): 
    user_data = test_user["user"]
    raw_password = test_user["password"]

    payload = {
        "email": user_data.email, 
        "password": raw_password 
    }


    response = await client.post("/auth/login", json=payload)


    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"