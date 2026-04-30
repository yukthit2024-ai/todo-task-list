package com.example.todomaster;

import android.app.AlertDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

public class MainFragment extends Fragment {

    private RecyclerView recyclerView;
    private MasterListAdapter adapter;
    private TodoMaster todoMaster;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_main, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        recyclerView = view.findViewById(R.id.recyclerView);
        FloatingActionButton fab = view.findViewById(R.id.fabAddList);

        todoMaster = XmlManager.read(requireContext());
        
        adapter = new MasterListAdapter(todoMaster.lists, list -> {
            int index = todoMaster.lists.indexOf(list);
            openDetailFragment(index);
        });

        recyclerView.setLayoutManager(new LinearLayoutManager(requireContext()));
        recyclerView.setAdapter(adapter);

        fab.setOnClickListener(v -> showAddListDialog());
    }

    private void openDetailFragment(int index) {
        Fragment fragment = ListDetailFragment.newInstance(index);
        requireActivity().getSupportFragmentManager().beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .addToBackStack(null)
            .commit();
    }

    private void showAddListDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
        builder.setTitle("New Master List");

        final EditText input = new EditText(requireContext());
        input.setHint("Enter list name");
        builder.setView(input);

        builder.setPositiveButton("Create", (dialog, which) -> {
            String name = input.getText().toString().trim();
            if (!name.isEmpty()) {
                TodoList newList = new TodoList(name);
                todoMaster.lists.add(newList);
                XmlManager.save(requireContext(), todoMaster);
                int index = todoMaster.lists.size() - 1;
                adapter.notifyItemInserted(index);
                openDetailFragment(index);
            } else {
                Toast.makeText(requireContext(), "Name cannot be empty", Toast.LENGTH_SHORT).show();
            }
        });

        builder.setNegativeButton("Cancel", (dialog, which) -> dialog.cancel());
        builder.show();
    }
}
