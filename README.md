# assessment-tracker-training-service

### Routes
- GET /associates
  - Gets all associates in the database
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
      }
  - Return 201 on success
    
- POST /associates/register
  - Creates a new associate_batch relationship
  - Accepts a JSON input:
    {
        "associateId": int,
        "batchId": int
    }
- GET /batches/<batch_id>
    - Get Batch with given batch ID
- GET /trainers/<trainer_id>/batches?year=<year>
    - Get all batches associated with the given trainer for the given year
- GET /trainers/<trainer_id>/batches?track=<track>
    - Get all batches associated with the given trainer for the given track
- POST /batches
    - Creates a new batch
    
- POST /notes
    - Creates a new note
- GET /notes
    - Get all notes
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
