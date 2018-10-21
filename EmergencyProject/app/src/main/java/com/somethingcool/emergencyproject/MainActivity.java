package com.somethingcool.emergencyproject;

import android.content.Context;
import android.content.Intent;
import android.location.LocationManager;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.google.firebase.FirebaseApp;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.somethingcool.emergencyproject.model.Hospital;
import com.somethingcool.emergencyproject.model.Location;
import com.somethingcool.emergencyproject.model.UserData;
import com.somethingcool.emergencyproject.network.MessagingService;
import com.somethingcool.emergencyproject.patient.PatientMainActivity;


public class MainActivity extends AppCompatActivity {

  Button patientButton;
  Button hospitalButton;

  LocationManager lm;
  private DatabaseReference mDatabase;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    patientButton = (Button) findViewById(R.id.patientButton);
    hospitalButton = (Button) findViewById(R.id.hospitalButton);
    patientButton.setOnClickListener(
        new View.OnClickListener() {
          @Override
          public void onClick(View v) {
            Intent i = new Intent(MainActivity.this, PatientMainActivity.class);
            startActivity(i);
          }
        });

    hospitalButton.setOnClickListener(
        new View.OnClickListener() {
          @Override
          public void onClick(View v) {
            Intent i = new Intent(MainActivity.this, Hospital.class);
            startActivity(i);
          }
        });
  }
}
