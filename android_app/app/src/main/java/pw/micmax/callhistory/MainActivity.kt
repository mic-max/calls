package pw.micmax.callhistory

import android.Manifest
import android.content.ContentValues
import android.content.Intent
import android.provider.CallLog.Calls
import android.widget.*
import android.os.*
import android.provider.MediaStore
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import com.google.protobuf.*
import java.io.*

class MainActivity : AppCompatActivity() {

    private lateinit var exportButton: Button

    private val requestPermissionLauncher = registerForActivityResult(ActivityResultContracts.RequestPermission()) {}

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        requestPermissionLauncher.launch(Manifest.permission.READ_CALL_LOG)

        exportButton = findViewById(R.id.exportButton)

        exportButton.setOnClickListener {
            val cursor = contentResolver.query(
                Calls.CONTENT_URI,
                arrayOf(Calls.DATE, Calls.NUMBER, Calls.TYPE, Calls.DURATION),
                null,
                null
            )

            if (cursor != null) {
                val callHistory = calls.Calls.CallHistory.newBuilder()

                val dateIndex = cursor.getColumnIndex(Calls.DATE)
                val numberIndex = cursor.getColumnIndex(Calls.NUMBER)
                val typeIndex = cursor.getColumnIndex(Calls.TYPE)
                val durationIndex = cursor.getColumnIndex(Calls.DURATION)

                while (cursor.moveToNext()) {
                    val call = calls.Calls.Call.newBuilder().apply {
                        this.start = Timestamp.newBuilder().setSeconds(cursor.getLong(dateIndex) / 1000).build()
                        this.number = cursor.getString(numberIndex)
                        this.type = calls.Calls.Call.CallType.forNumber(typeIndex)
                        this.duration = Duration.newBuilder().setSeconds(cursor.getLong(durationIndex)).build()
                    }.build()

                    callHistory.addCalls(call)
                }

                val history = callHistory.build()

                cursor.close()

                val intent = Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                    addCategory(Intent.CATEGORY_OPENABLE)
                    type = "application/octet-stream"
                    putExtra(Intent.EXTRA_TITLE, "call-history.bin")

                    // Optionally, specify a URI for the directory that should be opened in
                    // the system file picker before your app creates the document.
                    //putExtra(DocumentsContract.EXTRA_INITIAL_URI, pickerInitialUri)
                }
                startActivityForResult(intent, 1)


                try {
                    val filename = ""
                    val downloadCollection = MediaStore.Files.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)
                    val contentValues = ContentValues().apply() {
                        put(MediaStore.Files.FileColumns.DISPLAY_NAME, filename)
                    }
                    contentResolver.insert(downloadCollection, contentValues)?.also { uri ->
                        contentResolver.openOutputStream(uri).use { outputStream ->
                            history.writeTo(outputStream)
                            Toast.makeText(this, "Saved to ${uri.path}", Toast.LENGTH_LONG).show()
                        }
                    }

                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    }
}