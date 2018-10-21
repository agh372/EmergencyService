package com.somethingcool.emergencyproject.model;

import java.util.List;

public class UserData {
    private int userId;
    private String userName ;
    private String userLocation;

    public UserData(int userId, String userName, String userLocation) {
        this.userId = userId;
        this.userName = userName;
        this.userLocation = userLocation;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getUserLocation() {
        return userLocation;
    }

    public void setUserLocation(String userLocation) {
        this.userLocation = userLocation;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }
}