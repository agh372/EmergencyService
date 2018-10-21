package com.somethingcool.emergencyproject.patient;

import android.content.Context;
import android.location.LocationManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.google.firebase.FirebaseApp;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.messaging.FirebaseMessaging;
import com.google.firebase.messaging.RemoteMessage;
import com.somethingcool.emergencyproject.R;
import com.somethingcool.emergencyproject.model.Hospital;
import com.somethingcool.emergencyproject.model.Location;
import com.somethingcool.emergencyproject.model.UserData;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import butterknife.BindView;

public class PatientMainActivity extends AppCompatActivity {

  Button helpButton;

  private DatabaseReference mDatabase;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_patient_main);

      FirebaseApp.initializeApp(this);
      mDatabase = FirebaseDatabase.getInstance().getReference();

    helpButton = (Button) findViewById(R.id.helpButton);

      helpButton.setOnClickListener(
        new View.OnClickListener() {
          @Override
          public void onClick(View v) {
            writeNewUser();
          }
        });
   Log.d("TOKEN", FirebaseInstanceId.getInstance().getToken());

  }

  private void writeNewUser() {
    List<Integer> list = null;
    list = new ArrayList<>();

    for (int i = 0; i < 4; i++) {
      list.add(99 - i);
    }

    Random generator = new Random();
    int x = 10 - generator.nextInt(10);

    Random generator2 = new Random();
    int y = 10 - generator2.nextInt(10);

    Location location = new Location(x, y);

    UserData user = new UserData(111, "John Doe", x + "," + y);
    mDatabase.child("users").child(0 + "").setValue(user);

//    List hosList = new ArrayList();
//    for (int i = 0; i < 7; i++) {
//
//      Random generator3 = new Random();
//      x = 10 - generator.nextInt(10);
//
//      Random generator4 = new Random();
//      y = 10 - generator2.nextInt(10);
//      Location location2 = new Location(x, y);
//
//      Hospital hos1 = new Hospital(99 - i, "Hospital" + i, 3, x + "," + y);
//      hosList.add(hos1);
//    }
//    for (int i = 0; i < hosList.size(); i++) {
//      mDatabase.child("hospitals").child(i + "").setValue(hosList.get(i));
//    }
  }
}
