package com.somethingcool.emergencyproject.model;

public class Hospital {

    private int hospitalId;
    private String name ;
    private int resource ;
    private String hospitalLocation;


    public Hospital(int mHospitalId, String mName, int mResource, String hosLocation) {
        this.hospitalId = mHospitalId;
        this.name = mName;
        this.resource = mResource;
        this.hospitalLocation = hosLocation;
    }

    public int getHospitalId() {
        return hospitalId;
    }

    public void setHospitalId(int hospitalId) {
        this.hospitalId = hospitalId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getResource() {
        return resource;
    }

    public void setResource(int resource) {
        this.resource = resource;
    }

    public String getHospitalLocation() {
        return hospitalLocation;
    }

    public void setHospitalLocation(String hosLocation) {
        this.hospitalLocation = hosLocation;
    }
}
