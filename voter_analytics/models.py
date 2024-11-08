from django.db import models

# Create your models here.
class Votes(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    #residential address
    street_num = models.IntegerField()
    street_name = models.TextField()
    zip_code = models.IntegerField()
    #personal info
    DOB = models.DateField()
    DOR = models.DateField()
    party_affiliation = models.TextField()
    precinct_num = models.TextField()
    #vote result
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

def load_data():
    Votes.objects.all().delete()
    filename = 'newton_voters.csv'
    f = open(filename)
    f.readline()
    # line = f.readline().strip()
    # fields = line.split(',')
    # # show which value in each field
    # for i in range(len(fields)):
    #     print(f'fields[{i}] = {fields[i]}')
    for line in f:
        fields = line.split(',')
        try:
            votes = Votes(
                last_name = fields[1],
                first_name = fields[2],
                street_num = fields[3],
                street_name = fields[4],
                zip_code = fields[6],
                DOB = fields[7],
                DOR = fields[8],
                party_affiliation = fields[9].strip(),
                precinct_num = fields[10],
                v20state = fields[11].upper() == 'TRUE',
                v21town = fields[12].upper() == 'TRUE',
                v21primary = fields[13].upper() == 'TRUE',
                v22general = fields[14].upper() == 'TRUE',
                v23town = fields[15].upper() == 'TRUE',
                voter_score = fields[16],
            )
            votes.save()
            print(f'Created result: {votes}')
        except Exception as e:
            print(f"Skipped: {fields} due to {e}")
    print(f'Done. Created {len(Votes.objects.all())} Results.')
