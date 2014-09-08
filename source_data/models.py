from django.db import models
import hashlib
import random
from datetime import datetime

class EtlJob(models.Model):

    date_attempted = models.DateTimeField()
    date_completed = models.DateTimeField(null=True)
    task_name = models.CharField(max_length=55)
    status = models.CharField(max_length=10)
    guid = models.CharField(primary_key=True, max_length=40)

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        super(EtlJob, self).save(*args, **kwargs)


class ProcessStatus(models.Model):
    status_text = models.CharField(max_length=25)
    status_description = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.status_text)

    class Meta:
        app_label = 'source_data'


class VCMBirthRecord(models.Model):

    SubmissionDate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    DateOfReport = models.CharField(max_length=255)
    DateReport = models.CharField(max_length=255)
    SettlementCode = models.CharField(max_length=255)
    HouseHoldNumber = models.CharField(max_length=255)
    DOB = models.CharField(max_length=255)
    NameOfChild = models.CharField(max_length=255)
    VCM0Dose = models.CharField(max_length=255)
    VCMRILink = models.CharField(max_length=255)
    VCMNameCAttended = models.CharField(max_length=255)
    meta_instanceID = models.CharField(max_length=255)
    KEY = models.CharField(max_length=255,unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.NameOfChild)

    class Meta:
        app_label = 'source_data'

class VCMSummaryNew(models.Model):
    SubmissionDate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    DateOfReport = models.CharField(max_length=255)
    Date_Implement = models.CharField(max_length=255)
    SettlementCode = models.CharField(max_length=255)
    CensusNewBornsF = models.CharField(max_length=255)
    CensusNewBornsM = models.CharField(max_length=255)
    Tot_Newborns = models.CharField(max_length=255)
    Census2_11MoF = models.CharField(max_length=255)
    Census2_11MoM = models.CharField(max_length=255)
    Tot_2_11Months = models.CharField(max_length=255)
    Census12_59MoF = models.CharField(max_length=255)
    Census12_59MoM = models.CharField(max_length=255)
    Tot_12_59Months = models.CharField(max_length=255)
    Tot_Census = models.CharField(max_length=255)
    VaxNewBornsF = models.CharField(max_length=255)
    VaxNewBornsM = models.CharField(max_length=255)
    Tot_VaxNewBorn = models.CharField(max_length=255)
    display_vax2 = models.CharField(max_length=255)
    display_vax3 = models.CharField(max_length=255)
    display_vax1 = models.CharField(max_length=255)
    Vax2_11MoF = models.CharField(max_length=255)
    Vax2_11MoM = models.CharField(max_length=255)
    Tot_Vax2_11Mo = models.CharField(max_length=255)
    display_vax4 = models.CharField(max_length=255)
    display_vax5 = models.CharField(max_length=255)
    display_vax6 = models.CharField(max_length=255)
    Vax12_59MoF = models.CharField(max_length=255)
    Vax12_59MoM = models.CharField(max_length=255)
    Tot_Vax12_59Mo = models.CharField(max_length=255)
    Tot_Vax = models.CharField(max_length=255)
    Tot_Missed = models.CharField(max_length=255)
    display_vax7 = models.CharField(max_length=255)
    display_vax8 = models.CharField(max_length=255)
    display_vax9 = models.CharField(max_length=255)
    display_msd1 = models.CharField(max_length=255)
    display_msd2 = models.CharField(max_length=255)
    group_msd_chd_Msd_PlaygroundF = models.CharField(max_length=255)
    group_msd_chd_Msd_PlaygroundM = models.CharField(max_length=255)
    group_msd_chd_Msd_SocEventF = models.CharField(max_length=255)
    group_msd_chd_Msd_SocEventM = models.CharField(max_length=255)
    group_msd_chd_Msd_MarketF = models.CharField(max_length=255)
    group_msd_chd_Msd_MarketM = models.CharField(max_length=255)
    group_msd_chd_Msd_FarmF = models.CharField(max_length=255)
    group_msd_chd_Msd_FarmM = models.CharField(max_length=255)
    group_msd_chd_Msd_SchoolF = models.CharField(max_length=255)
    group_msd_chd_Msd_SchoolM = models.CharField(max_length=255)
    group_msd_chd_Msd_ChildSickF = models.CharField(max_length=255)
    group_msd_chd_Msd_ChildSickM = models.CharField(max_length=255)
    group_msd_chd_Msd_SideEffectsF = models.CharField(max_length=255)
    group_msd_chd_Msd_SideEffectsM = models.CharField(max_length=255)
    group_msd_chd_Msd_NoFeltNeedF = models.CharField(max_length=255)
    group_msd_chd_Msd_NoFeltNeedM = models.CharField(max_length=255)
    group_msd_chd_Msd_TooManyRoundsF = models.CharField(max_length=255)
    group_msd_chd_Msd_TooManyRoundsM = models.CharField(max_length=255)
    group_msd_chd_Msd_RelBeliefsF = models.CharField(max_length=255)
    group_msd_chd_Msd_RelBeliefsM = models.CharField(max_length=255)
    group_msd_chd_Msd_PolDiffsF = models.CharField(max_length=255)
    group_msd_chd_Msd_PolDiffsM = models.CharField(max_length=255)
    group_msd_chd_Msd_UnhappyWTeamF = models.CharField(max_length=255)
    group_msd_chd_Msd_UnhappyWTeamM = models.CharField(max_length=255)
    group_msd_chd_Msd_NoPlusesF = models.CharField(max_length=255)
    group_msd_chd_Msd_NoPlusesM = models.CharField(max_length=255)
    group_msd_chd_Msd_NoGovtServicesF = models.CharField(max_length=255)
    group_msd_chd_Msd_NoGovtServicesM = models.CharField(max_length=255)
    group_msd_chd_Msd_PolioUncommonF = models.CharField(max_length=255)
    group_msd_chd_Msd_PolioUncommonM = models.CharField(max_length=255)
    group_msd_chd_Msd_PolioHasCureF = models.CharField(max_length=255)
    group_msd_chd_Msd_PolioHasCureM = models.CharField(max_length=255)
    group_msd_chd_Msd_OtherProtectionF = models.CharField(max_length=255)
    group_msd_chd_Msd_OtherProtectionM = models.CharField(max_length=255)
    group_msd_chd_Msd_NoConsentF = models.CharField(max_length=255)
    group_msd_chd_Msd_NoConsentM = models.CharField(max_length=255)
    group_msd_chd_Msd_HHNotVisitedF = models.CharField(max_length=255)
    group_msd_chd_Msd_HHNotVisitedM = models.CharField(max_length=255)
    group_msd_chd_Msd_SecurityF = models.CharField(max_length=255)
    group_msd_chd_Msd_SecurityM = models.CharField(max_length=255)
    group_msd_chd_Msd_AgedOutF = models.CharField(max_length=255)
    group_msd_chd_Msd_AgedOutM = models.CharField(max_length=255)
    group_msd_chd_Msd_FamilyMovedF = models.CharField(max_length=255)
    group_msd_chd_Msd_FamilyMovedM = models.CharField(max_length=255)
    group_msd_chd_Msd_ChildDiedF = models.CharField(max_length=255)
    group_msd_chd_Msd_ChildDiedM = models.CharField(max_length=255)
    group_msd_chd_Tot_Missed_Check = models.CharField(max_length=255)
    group_msd_chd_display_msd3 = models.CharField(max_length=255)
    spec_grp_choice = models.CharField(max_length=255)
    group_spec_events_Spec_ZeroDose = models.CharField(max_length=255)
    group_spec_events_Spec_PregnantMother = models.CharField(max_length=255)
    group_spec_events_Spec_Newborn = models.CharField(max_length=255)
    group_spec_events_Spec_VCMAttendedNCer = models.CharField(max_length=255)
    group_spec_events_Spec_CMAMReferral = models.CharField(max_length=255)
    group_spec_events_Spec_RIReferral = models.CharField(max_length=255)
    group_spec_events_Spec_AFPCase = models.CharField(max_length=255)
    group_spec_events_Spec_MslsCase = models.CharField(max_length=255)
    group_spec_events_Spec_OtherDisease = models.CharField(max_length=255)
    group_spec_events_Spec_FIC = models.CharField(max_length=255)
    meta_instanceID = models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('Hello')

    class Meta:
        app_label = 'source_data'


class VCMSettlement(models.Model):

    SubmissionDate = models.CharField(max_length=255)
    deviceid = models.CharField(max_length=255)
    simserial = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    DateRecorded = models.CharField(max_length=255)
    SettlementCode = models.CharField(max_length=255)
    SettlementName = models.CharField(max_length=255)
    VCMName = models.CharField(max_length=255)
    VCMPhone = models.CharField(max_length=255)
    SettlementGPS_Latitude = models.CharField(max_length=255)
    SettlementGPS_Longitude = models.CharField(max_length=255)
    SettlementGPS_Altitude = models.CharField(max_length=255)
    SettlementGPS_Accuracy = models.CharField(max_length=255)
    meta_instanceID = models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at  = models.DateTimeField(default=datetime.now())


    def __unicode__(self):
        return unicode(self.SettlementName)

    class Meta:
        app_label = 'source_data'


class VCMSummaryOld(models.Model):
    SubmissionDate=models.CharField(max_length=255)
    deviceid=models.CharField(max_length=255)
    simserial=models.CharField(max_length=255)
    phonenumber=models.CharField(max_length=255)
    DateOfReport=models.CharField(max_length=255)
    Date_Implement=models.CharField(max_length=255)
    SettlementCode=models.CharField(max_length=255)
    CensusNewBornsF=models.CharField(max_length=255)
    CensusNewBornsM=models.CharField(max_length=255)
    Census2_11MoF=models.CharField(max_length=255)
    Census2_11MoM=models.CharField(max_length=255)
    Census12_59MoF=models.CharField(max_length=255)
    Census12_59MoM=models.CharField(max_length=255)
    VaxNewBornsF=models.CharField(max_length=255)
    VaxNewBornsM=models.CharField(max_length=255)
    Vax2_11MoF=models.CharField(max_length=255)
    Vax2_11MoM=models.CharField(max_length=255)
    Vax12_59MoF=models.CharField(max_length=255)
    Vax12_59MoM=models.CharField(max_length=255)
    Msd_grp_choice=models.CharField(max_length=255)
    group_msd_chd_Msd_PlaygroundF=models.CharField(max_length=255)
    group_msd_chd_Msd_PlaygroundM=models.CharField(max_length=255)
    group_msd_chd_Msd_SocEventF=models.CharField(max_length=255)
    group_msd_chd_Msd_SocEventM=models.CharField(max_length=255)
    group_msd_chd_Msd_MarketF=models.CharField(max_length=255)
    group_msd_chd_Msd_MarketM=models.CharField(max_length=255)
    group_msd_chd_Msd_FarmF=models.CharField(max_length=255)
    group_msd_chd_Msd_FarmM=models.CharField(max_length=255)
    group_msd_chd_Msd_SchoolF=models.CharField(max_length=255)
    group_msd_chd_Msd_SchoolM=models.CharField(max_length=255)
    group_msd_chd_Msd_ChildSickF=models.CharField(max_length=255)
    group_msd_chd_Msd_ChildSickM=models.CharField(max_length=255)
    group_msd_chd_Msd_SideEffectsF=models.CharField(max_length=255)
    group_msd_chd_Msd_SideEffectsM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoFeltNeedF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoFeltNeedM=models.CharField(max_length=255)
    group_msd_chd_Msd_TooManyRoundsF=models.CharField(max_length=255)
    group_msd_chd_Msd_TooManyRoundsM=models.CharField(max_length=255)
    group_msd_chd_Msd_RelBeliefsF=models.CharField(max_length=255)
    group_msd_chd_Msd_RelBeliefsM=models.CharField(max_length=255)
    group_msd_chd_Msd_PolDiffsF=models.CharField(max_length=255)
    group_msd_chd_Msd_PolDiffsM=models.CharField(max_length=255)
    group_msd_chd_Msd_UnhappyWTeamF=models.CharField(max_length=255)
    group_msd_chd_Msd_UnhappyWTeamM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoPlusesF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoPlusesM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoGovtServicesF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoGovtServicesM=models.CharField(max_length=255)
    group_msd_chd_Msd_PolioUncommonF=models.CharField(max_length=255)
    group_msd_chd_Msd_PolioUncommonM=models.CharField(max_length=255)
    group_msd_chd_Msd_PolioHasCureF=models.CharField(max_length=255)
    group_msd_chd_Msd_PolioHasCureM=models.CharField(max_length=255)
    group_msd_chd_Msd_OtherProtectionF=models.CharField(max_length=255)
    group_msd_chd_Msd_OtherProtectionM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoConsentF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoConsentM=models.CharField(max_length=255)
    group_msd_chd_Msd_HHNotVisitedF=models.CharField(max_length=255)
    group_msd_chd_Msd_HHNotVisitedM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoReasonF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoReasonM=models.CharField(max_length=255)
    group_msd_chd_Msd_SecurityF=models.CharField(max_length=255)
    group_msd_chd_Msd_SecurityM=models.CharField(max_length=255)
    group_msd_chd_Msd_AgedOutF=models.CharField(max_length=255)
    group_msd_chd_Msd_AgedOutM=models.CharField(max_length=255)
    group_msd_chd_Msd_FamilyMovedF=models.CharField(max_length=255)
    group_msd_chd_Msd_FamilyMovedM=models.CharField(max_length=255)
    group_msd_chd_Msd_ChildDiedF=models.CharField(max_length=255)
    group_msd_chd_Msd_ChildDiedM=models.CharField(max_length=255)
    spec_grp_choice=models.CharField(max_length=255)
    group_spec_events_Spec_ZeroDose=models.CharField(max_length=255)
    group_spec_events_Spec_PregnantMother=models.CharField(max_length=255)
    group_spec_events_Spec_Newborn=models.CharField(max_length=255)
    group_spec_events_Spec_VCMAttendedNCer=models.CharField(max_length=255)
    group_spec_events_Spec_CMAMReferral=models.CharField(max_length=255)
    group_spec_events_Spec_RIReferral=models.CharField(max_length=255)
    group_spec_events_Spec_AFPCase=models.CharField(max_length=255)
    group_spec_events_Spec_MslsCase=models.CharField(max_length=255)
    group_spec_events_Spec_OtherDisease=models.CharField(max_length=255)
    group_spec_events_Spec_FIC=models.CharField(max_length=255)
    meta_instanceID=models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class ClusterSupervisor(models.Model):
    SubmissionDate=models.CharField(max_length=255)
    DateRecorded=models.CharField(max_length=255)
    start_time=models.CharField(max_length=255)
    end_time=models.CharField(max_length=255)
    instruction=models.CharField(max_length=255)
    supervision_location_Latitude=models.CharField(max_length=255)
    supervision_location_Longitude=models.CharField(max_length=255)
    supervision_location_Altitude=models.CharField(max_length=255)
    supervision_location_Accuracy=models.CharField(max_length=255)
    supervisor_title=models.CharField(max_length=255)
    supervisor_name=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    lga=models.CharField(max_length=255)
    supervisee_name=models.CharField(max_length=255)
    num_LGAC=models.CharField(max_length=255)
    hrop_endorsed=models.CharField(max_length=255)
    hrop_socialdata=models.CharField(max_length=255)
    hrop_special_pop=models.CharField(max_length=255)
    hrop_activities_planned=models.CharField(max_length=255)
    hrop_activities_conducted=models.CharField(max_length=255)
    hrop_implementation=models.CharField(max_length=255)
    hrop_workplan_aligned=models.CharField(max_length=255)
    coord_smwg_meetings=models.CharField(max_length=255)
    coord_vcm_meeting=models.CharField(max_length=255)
    coord_rfp_meeting=models.CharField(max_length=255)
    vcm_supervision=models.CharField(max_length=255)
    vcm_data=models.CharField(max_length=255)
    vcm_birthtracking=models.CharField(max_length=255)
    ri_supervision=models.CharField(max_length=255)
    fund_transparency=models.CharField(max_length=255)
    meta_instanceID=models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class PhoneInventory(models.Model):
    SubmissionDate=models.CharField(max_length=255)
    meta_instanceID=models.CharField(max_length=255)
    Name=models.CharField(max_length=255)
    State=models.CharField(max_length=255)
    LGA=models.CharField(max_length=255)
    Colour_phone=models.CharField(max_length=255)
    Asset_number=models.CharField(max_length=255)
    telephone_no=models.CharField(max_length=255)
    DeviceID=models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class ActivityReport(models.Model):
    SubmissionDate=models.CharField(max_length=255)
    DateRecorded=models.CharField(max_length=255)
    start_time=models.CharField(max_length=255)
    endtime=models.CharField(max_length=255)
    SettlementGPS_Latitude=models.CharField(max_length=255)
    SettlementGPS_Longitude=models.CharField(max_length=255)
    SettlementGPS_Altitude=models.CharField(max_length=255)
    SettlementGPS_Accuracy=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    lga=models.CharField(max_length=255)
    ward=models.CharField(max_length=255)
    settlementname=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    names=models.CharField(max_length=255)
    activity=models.CharField(max_length=255)
    hc_townannouncer=models.CharField(max_length=255)
    hc_opvvaccinator=models.CharField(max_length=255)
    hc_recorder_opv=models.CharField(max_length=255)
    hc_separatetally=models.CharField(max_length=255)
    hc_clinician1=models.CharField(max_length=255)
    hc_clinician2=models.CharField(max_length=255)
    hc_recorder_ri=models.CharField(max_length=255)
    hc_crowdcontroller=models.CharField(max_length=255)
    hc_nc_location=models.CharField(max_length=255)
    hc_appropriate_location=models.CharField(max_length=255)
    hc_stockout=models.CharField(max_length=255)
    hc_num_opv=models.CharField(max_length=255)
    hc_num_measles=models.CharField(max_length=255)
    hc_num_penta=models.CharField(max_length=255)
    hc_num_patients=models.CharField(max_length=255)
    hc_team_allowances=models.CharField(max_length=255)
    cd_attendance=models.CharField(max_length=255)
    cd_num_hh_affected=models.CharField(max_length=255)
    cd_local_leadership_present=models.CharField(max_length=255)
    cd_resolved=models.CharField(max_length=255)
    cd_hh_pending_issues=models.CharField(max_length=255)
    cd_num_vaccinated=models.CharField(max_length=255)
    cd_iec=models.CharField(max_length=255)
    cd_pro_opv_cd=models.CharField(max_length=255)
    cm_attendance=models.CharField(max_length=255)
    cm_num_husband_issues=models.CharField(max_length=255)
    cm_num_caregiver_issues=models.CharField(max_length=255)
    cm_VCM_sett=models.CharField(max_length=255)
    cm_VCM_present=models.CharField(max_length=255)
    cm_iec=models.CharField(max_length=255)
    cm_num_vaccinated=models.CharField(max_length=255)
    cm_num_positive=models.CharField(max_length=255)
    ipds_team=models.CharField(max_length=255)
    ipds_issue_reported=models.CharField(max_length=255)
    ipds_other_issue=models.CharField(max_length=255)
    ipds_num_hh=models.CharField(max_length=255)
    ipds_num_children=models.CharField(max_length=255)
    ipds_issue_resolved=models.CharField(max_length=255)
    ipds_team_allowances=models.CharField(max_length=255)
    ipds_community_leader_present=models.CharField(max_length=255)
    meta_instanceID=models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class VWSRegister(models.Model):
    SubmissionDate=models.CharField(max_length=255)
    deviceid=models.CharField(max_length=255)
    simserial=models.CharField(max_length=255)
    phonenumber=models.CharField(max_length=255)
    DatePhoneCollected=models.CharField(max_length=255)
    FName_VWS=models.CharField(max_length=255)
    LName_VWS=models.CharField(max_length=255)
    WardCode=models.CharField(max_length=255)
    Personal_Phone=models.CharField(max_length=255)
    AcceptPhoneResponsibility=models.CharField(max_length=255)
    meta_instanceID=models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class HealthCamp(models.Model):
    region = models.CharField(max_length=255)
    SubmissionDate=models.CharField(max_length=255)
    formhub_uuid=models.CharField(max_length=255)
    phonenumber=models.CharField(max_length=255)
    userid=models.CharField(max_length=255)
    DateRecorded=models.CharField(max_length=255)
    start_time=models.CharField(max_length=255)
    lga=models.CharField(max_length=255)
    ward=models.CharField(max_length=255)
    settlementname=models.CharField(max_length=255)
    names=models.CharField(max_length=255)
    agencyname=models.CharField(max_length=255)
    townannouncer=models.CharField(max_length=255)
    megaphone=models.CharField(max_length=255)
    opvvaccinator=models.CharField(max_length=255)
    recorder_opv=models.CharField(max_length=255)
    separatetally=models.CharField(max_length=255)
    clinician1=models.CharField(max_length=255)
    clinician2=models.CharField(max_length=255)
    recorder_ri=models.CharField(max_length=255)
    crowdcontroller=models.CharField(max_length=255)
    nc_location=models.CharField(max_length=255)
    appropriate_location=models.CharField(max_length=255)
    hc_stockout=models.CharField(max_length=255)
    num_opv=models.CharField(max_length=255)
    num_measles=models.CharField(max_length=255)
    num_penta=models.CharField(max_length=255)
    num_patients=models.CharField(max_length=255)
    hc_photo=models.CharField(max_length=255)
    SettlementGPS_Latitude=models.CharField(max_length=255)
    SettlementGPS_Longitude=models.CharField(max_length=255)
    SettlementGPS_Altitude=models.CharField(max_length=255)
    SettlementGPS_Accuracy=models.CharField(max_length=255)
    endtime=models.CharField(max_length=255)
    meta_instanceID=models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class PracticeVCMSettCoordinates(models.Model):
    SubmissionDate=models.CharField(max_length=255)
    deviceid=models.CharField(max_length=255)
    simserial=models.CharField(max_length=255)
    phonenumber=models.CharField(max_length=255)
    DateRecorded=models.CharField(max_length=255)
    SettlementCode=models.CharField(max_length=255)
    SettlementName=models.CharField(max_length=255)
    VCMName=models.CharField(max_length=255)
    VCMPhone=models.CharField(max_length=255)
    SettlementGPS_Latitude=models.CharField(max_length=255)
    SettlementGPS_Longitude=models.CharField(max_length=255)
    SettlementGPS_Altitude=models.CharField(max_length=255)
    SettlementGPS_Accuracy=models.CharField(max_length=255)
    meta_instanceID=models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class PaxListReportTraining(models.Model):
    SubmissionDate=models.CharField(max_length=255)
    meta_instanceID=models.CharField(max_length=255)
    State=models.CharField(max_length=255)
    NameOfParticipant=models.CharField(max_length=255)
    Title=models.CharField(max_length=255)
    PhoneNumber=models.CharField(max_length=255)
    EmailAddr=models.CharField(max_length=255)
    TimeStamp=models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'


class PracticeVCMSummary(models.Model):
    SubmissionDate=models.CharField(max_length=255)
    deviceid=models.CharField(max_length=255)
    simserial=models.CharField(max_length=255)
    phonenumber=models.CharField(max_length=255)
    DateOfReport=models.CharField(max_length=255)
    Date_Implement=models.CharField(max_length=255)
    SettlementCode=models.CharField(max_length=255)
    CensusNewBornsF=models.CharField(max_length=255)
    CensusNewBornsM=models.CharField(max_length=255)
    Census2_11MoF=models.CharField(max_length=255)
    Census2_11MoM=models.CharField(max_length=255)
    Census12_59MoF=models.CharField(max_length=255)
    Census12_59MoM=models.CharField(max_length=255)
    VaxNewBornsF=models.CharField(max_length=255)
    VaxNewBornsM=models.CharField(max_length=255)
    Vax2_11MoF=models.CharField(max_length=255)
    Vax2_11MoM=models.CharField(max_length=255)
    Vax12_59MoF=models.CharField(max_length=255)
    Vax12_59MoM=models.CharField(max_length=255)
    Msd_grp_choice=models.CharField(max_length=255)
    group_msd_chd_Msd_PlaygroundF=models.CharField(max_length=255)
    group_msd_chd_Msd_PlaygroundM=models.CharField(max_length=255)
    group_msd_chd_Msd_SocEventF=models.CharField(max_length=255)
    group_msd_chd_Msd_SocEventM=models.CharField(max_length=255)
    group_msd_chd_Msd_MarketF=models.CharField(max_length=255)
    group_msd_chd_Msd_MarketM=models.CharField(max_length=255)
    group_msd_chd_Msd_FarmF=models.CharField(max_length=255)
    group_msd_chd_Msd_FarmM=models.CharField(max_length=255)
    group_msd_chd_Msd_SchoolF=models.CharField(max_length=255)
    group_msd_chd_Msd_SchoolM=models.CharField(max_length=255)
    group_msd_chd_Msd_ChildSickF=models.CharField(max_length=255)
    group_msd_chd_Msd_ChildSickM=models.CharField(max_length=255)
    group_msd_chd_Msd_SideEffectsF=models.CharField(max_length=255)
    group_msd_chd_Msd_SideEffectsM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoFeltNeedF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoFeltNeedM=models.CharField(max_length=255)
    group_msd_chd_Msd_TooManyRoundsF=models.CharField(max_length=255)
    group_msd_chd_Msd_TooManyRoundsM=models.CharField(max_length=255)
    group_msd_chd_Msd_RelBeliefsF=models.CharField(max_length=255)
    group_msd_chd_Msd_RelBeliefsM=models.CharField(max_length=255)
    group_msd_chd_Msd_PolDiffsF=models.CharField(max_length=255)
    group_msd_chd_Msd_PolDiffsM=models.CharField(max_length=255)
    group_msd_chd_Msd_UnhappyWTeamF=models.CharField(max_length=255)
    group_msd_chd_Msd_UnhappyWTeamM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoPlusesF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoPlusesM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoGovtServicesF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoGovtServicesM=models.CharField(max_length=255)
    group_msd_chd_Msd_PolioUncommonF=models.CharField(max_length=255)
    group_msd_chd_Msd_PolioUncommonM=models.CharField(max_length=255)
    group_msd_chd_Msd_PolioHasCureF=models.CharField(max_length=255)
    group_msd_chd_Msd_PolioHasCureM=models.CharField(max_length=255)
    group_msd_chd_Msd_OtherProtectionF=models.CharField(max_length=255)
    group_msd_chd_Msd_OtherProtectionM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoConsentF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoConsentM=models.CharField(max_length=255)
    group_msd_chd_Msd_HHNotVisitedF=models.CharField(max_length=255)
    group_msd_chd_Msd_HHNotVisitedM=models.CharField(max_length=255)
    group_msd_chd_Msd_NoReasonF=models.CharField(max_length=255)
    group_msd_chd_Msd_NoReasonM=models.CharField(max_length=255)
    group_msd_chd_Msd_SecurityF=models.CharField(max_length=255)
    group_msd_chd_Msd_SecurityM=models.CharField(max_length=255)
    group_msd_chd_Msd_AgedOutF=models.CharField(max_length=255)
    group_msd_chd_Msd_AgedOutM=models.CharField(max_length=255)
    group_msd_chd_Msd_FamilyMovedF=models.CharField(max_length=255)
    group_msd_chd_Msd_FamilyMovedM=models.CharField(max_length=255)
    group_msd_chd_Msd_ChildDiedF=models.CharField(max_length=255)
    group_msd_chd_Msd_ChildDiedM=models.CharField(max_length=255)
    spec_grp_choice=models.CharField(max_length=255)
    group_spec_events_Spec_ZeroDose=models.CharField(max_length=255)
    group_spec_events_Spec_PregnantMother=models.CharField(max_length=255)
    group_spec_events_Spec_Newborn=models.CharField(max_length=255)
    group_spec_events_Spec_VCMAttendedNCer=models.CharField(max_length=255)
    group_spec_events_Spec_CMAMReferral=models.CharField(max_length=255)
    group_spec_events_Spec_RIReferral=models.CharField(max_length=255)
    group_spec_events_Spec_AFPCase=models.CharField(max_length=255)
    group_spec_events_Spec_MslsCase=models.CharField(max_length=255)
    group_spec_events_Spec_OtherDisease=models.CharField(max_length=255)
    group_spec_events_Spec_FIC=models.CharField(max_length=255)
    meta_instanceID=models.CharField(max_length=255)
    KEY = models.CharField(max_length=255, unique=True)
    process_status = models.ForeignKey(ProcessStatus)
    request_guid = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode('hello')

    class Meta:
        app_label = 'source_data'
