
public class FiltersOperatorsOn extends RecordFilterOperatorsTest {
	
	SimpleDateFormat dateFormatter = new SimpleDateFormat ("yyyy-MM-dd HH:mm:ss");
	
	public static int NUMBER_OF_RECORDS_Now = 19;
	public static int NUMBER_OF_RECORDS_OneHourAgo = 17;
	public static int NUMBER_OF_RECORDS_Yesterday = 13;
	public static int NUMBER_OF_RECORDS_LastWeek = 11;
	public static int NUMBER_OF_RECORDS_LastMonth = 7;
	public static int NUMBER_OF_RECORDS_ThreeMonthsAgo = 5;
	public static int NUMBER_OF_RECORDS_LastYear = 3;
	
	public Calendar now = new GregorianCalendar();
	public Calendar now2 = new GregorianCalendar();

    //the actual url values are removed for reprinting the code segment in the book
    public static String url_for_last_week = ""; 
    public static String url_for_last_year = "";
	
	@BeforeClass
	public void setupData () { 
        // get time zone in the application
        timezone = getTimeZone();
		// now is used to create the data.
		now = Calendar.getInstance(timezone);
		// now2 is used to get the current time in the tests.
		now2 = Calendar.getInstance(timezone);
	
		// for all existing RECORDS, set the 'Release time' to 2 years ago, so they won't interfere with the tests.
		Calendar aYearAgo = ((Calendar) now.clone());
		aYearAgo.add(Calendar.YEAR, -2);
        modifyTableRecords ("Release_time", dateFormatter.format((aYearAgo.getTime())).toString());
		
		// create various numbers of RECORDS with different 'Release time' for the tests.
		Calendar calNow = ((Calendar) now.clone());
	    String Release_time_Now = dateFormatter.format(calNow.getTime());
	    for (int i = 0; i < NUMBER_OF_RECORDS_Now; i++) {
			createRecord("Release_time_Now", "New", 0, Release_time_Now.toString(), true);
		}
	        
        Calendar calOneHourAgo = ((Calendar) now.clone());
        calOneHourAgo.add(Calendar.MINUTE, -30);
        String Release_time_OneHourAgo = dateFormatter.format(calOneHourAgo.getTime());
        for (int i = 0; i < NUMBER_OF_RECORDS_OneHourAgo; i++) {
			createRecord("Release_time_OneHourAgo", "New", 1, Release_time_OneHourAgo.toString(), true);
		}
        
        Calendar calYesteday = ((Calendar) now.clone());
        calYesteday.add(Calendar.DAY_OF_YEAR, -1);
        String Release_time_Yesterday = dateFormatter.format(calYesteday.getTime());
        for (int i = 0; i < NUMBER_OF_RECORDS_Yesterday; i++) {
			createRecord("Release_time_Yesterday", "Awaiting", 2, Release_time_Yesterday.toString(), false);
		}
        
        Calendar calLastWeek = ((Calendar) now.clone());
        calLastWeek.add(Calendar.WEEK_OF_YEAR, -1);
        String Release_time_LastWeek = dateFormatter.format(calLastWeek.getTime());
        for (int i = 0; i < NUMBER_OF_RECORDS_LastWeek; i++) {
			createRecord("Release_time_LastWeek", "Resolved", 5, Release_time_LastWeek.toString(), true);
		}
			
        Calendar calLastMonth = ((Calendar) now.clone());
        calLastMonth.add(Calendar.MONTH, -1);
        String Release_time_LastMonth = dateFormatter.format(calLastMonth.getTime());
        for (int i = 0; i < NUMBER_OF_RECORDS_LastMonth; i++) {
			createRecord("Release_time_LastMonth", "Closed", 8, Release_time_LastMonth.toString(), true);
		}
        
        Calendar calThreeMonthsAgo = ((Calendar) now.clone());
        calThreeMonthsAgo.add(Calendar.MONTH, -3);
        if (calThreeMonthsAgo.get(Calendar.DAY_OF_MONTH) > 1)
        	calThreeMonthsAgo.add(Calendar.DAY_OF_YEAR, -1); //to count for any confusion if Feb has 28 days.
        String Release_time_ThreeMonthsAgo = dateFormatter.format(calThreeMonthsAgo.getTime());
        for (int i = 0; i < NUMBER_OF_RECORDS_ThreeMonthsAgo; i++) {
			createRecord("Release_time_ThreeMonthsAgo", "New", 0, Release_time_ThreeMonthsAgo.toString(), true);
		}
        
        Calendar calLastYear = ((Calendar) now.clone());
        calLastYear.add(Calendar.YEAR, -1);
        String Release_time_LastYear = dateFormatter.format(calLastYear.getTime());
        for (int i = 0; i < NUMBER_OF_RECORDS_LastYear; i++) {
			createRecord("Release_time_LastYear", "Awaiting", 3, Release_time_LastYear.toString(), true);
		}
	}
	
	@Test
	// test case 5: records have "Release time" on 'last week'.
	public void testFilterOperatorOnDateTimeLastWeek() throws Exception  {
		openNavURI(url_for_last_week);
		int NumOFRecordReturned = getNumOfRecordsOnFilteringResult();
		// if the current date is the 1st day of the week (Monday), then the records created yesterday is from last week: a week is from Mon to Sun.
		if (now2.get(Calendar.DAY_OF_WEEK) == Calendar.MONDAY ) {
			if (now2.get(Calendar.HOUR) == 0 && now.get(Calendar.MINUTE) < 30) {
				assertEquals(NUMBER_OF_RECORDS_LastWeek + NUMBER_OF_RECORDS_Yesterday + NUMBER_OF_RECORDS_OneHourAgo, NumOFRecordReturned);
			}
			else {  assertEquals(NUMBER_OF_RECORDS_LastWeek + NUMBER_OF_RECORDS_Yesterday, NumOFRecordReturned); }
		}
		else {  assertEquals(NUMBER_OF_RECORDS_LastWeek, NumOFRecordReturned); }

		// validate the date is last week for the records created last week.
		for (int i = 0; i< NumOFRecordReturned; i++) {
			String ReleaseTimeOnUI = getCellValue("release_time", i+1);
			Date ReleaseTimeDate = dateFormatter.parse(ReleaseTimeOnUI);
			Calendar calReleaseTimeDate = Calendar.getInstance();
			calReleaseTimeDate.setTime(ReleaseTimeDate);

			// a week starts from Monday in this application, while in Java Calendar, a week starts from Sunday.
			boolean isMonday = now2.get(Calendar.DAY_OF_WEEK) == Calendar.MONDAY;
			int weekOfYearDiff = now2.get(Calendar.WEEK_OF_YEAR) - calReleaseTimeDate.get(Calendar.WEEK_OF_YEAR);
			Assert.assertTrue(
					(isMonday && weekOfYearDiff == 0) // this week and it is Monday
					|| weekOfYearDiff == 1 // week before
					|| weekOfYearDiff == -51 // week before but this is a new year
			);
		}
	}
	
	@Test
	// test case 14: records have "Release time" on 'last year'.
	public void testFilterOperatorOnDateTimeLastYear() throws Exception  {
		openNavURI(url_for_last_year);
        int NumOFRecordReturned = getNumOfRecordsOnFilteringResult();
		
		for (int i = 0; i< NumOFRecordReturned; i++) {
			String ReleaseTimeOnUI = getCellValue("release_time", i+1);
			Date ReleaseTimeDate = dateFormatter.parse(ReleaseTimeOnUI);
			Calendar calReleaseTimeDate = Calendar.getInstance();
			calReleaseTimeDate.setTime(ReleaseTimeDate);
			
			Assert.assertTrue( (now2.get(Calendar.YEAR) - calReleaseTimeDate.get(Calendar.YEAR) == 1) );		
		}
	}

    // create table record (only the signature is shown here)
    public void createRecord(String description, String state, int change_count, String release_time, Boolean active) {
	}

	@AfterClass
	public void disposeEnvironment() {
	}
}
