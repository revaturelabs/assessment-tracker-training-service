# assessment-tracker-training-service

### Routes
- GET /associates/<associate_id>
  - Get associate with given ID
  - Returns 200 on success, 404 on invalid ID
- GET /batches/<batch_id>/associates
  - Get all associates in given batch_id
  - Returns 200 on success, 404 on invalid batch ID
- POST /associates
  - Creates a new associate 
  -   Accepts a JSON input:
      {
          "firstName": str,
          "lastName": str,
          "email": str,
          "trainingStatus": str,
          "batchId": int
      }
  - Return 201 on success
- GET /batches/<batch_id>
    - Get Batch with given batch ID
- GET /batches?trainerId=<trainer_id>&year=<year>
    - Get all batches associated with the given trainer for the given year
- GET /batches?trainerId=<trainer_id>&track=<track>
    - Get all batches associated with the given trainer for the given track
- POST /batches
    - Creates a new batch
    
- POST /notes
    - Creates a new note
- GET /notes
    - Get all notes
- GET /notes?traineeId=<trainee_id>
    - Get all notes for the given trainee
- GET /associates/<associate_id>/notes
    - Get all notes for a specific associate
- GET /associates/<associate_id>/notes?week=<week>
    - Get all notes for a specific associate for a specified week
- PUT /notes/<note_id>
    - Update given note
- DELETE /notes/<note_id>
    - Delete given note
- POST /trainers
    - Create a new trainer object
- GET /trainers/<trainer_id>
    - Get a trainer by ID
- GET /batches/<batch_id>/trainers
    - Get all trainers associated with a given batch
- GET years?trainerId=<trainer_id>
    - Get all years in which a given trainer had batches