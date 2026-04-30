package com.vypeensoft.todo;

import android.os.Bundle;
import android.view.MenuItem;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

public class AboutActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about);

        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("About");
        }

        TextView tvVersion = findViewById(R.id.tv_version);
        TextView tvBuildDate = findViewById(R.id.tv_build_date);
        TextView tvGitSha = findViewById(R.id.tv_git_sha);
        TextView tvGitTag = findViewById(R.id.tv_git_tag);

        tvVersion.setText("Version " + BuildConfig.VERSION_NAME);
        tvBuildDate.setText(BuildConfig.BUILD_TIMESTAMP);
        tvGitSha.setText(BuildConfig.GIT_SHA);
        tvGitTag.setText(BuildConfig.GIT_TAG != null && !BuildConfig.GIT_TAG.isEmpty() ? BuildConfig.GIT_TAG : "N/A");
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == android.R.id.home) {
            onBackPressed();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
