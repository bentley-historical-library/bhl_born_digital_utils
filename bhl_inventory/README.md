# BHL Inventory

A tracking template used for born-digital transfers at the Bentley Historical Library.

## Pre-transfer
- accession_num
- barcode
- sequence_num
- physical_loc (Removable Media Dropbox, BHL `_box location_`, NCRC `_box location_`)
- media_type (5.25'' floppy, 3.5'' floppy, data CD, data DVD, audio CD, video DVD, USB, External HDD)
- examiner (`_UM uniqname_`)
- took_photo (Y, N, N/A)
- printed_notice (Y, N, N/A)

## Transfer
- pass_1_successful (Y, N, N/A)
- pass_1_date (YYYY-MM-DD)
- pass_2_successful (Y, N, N/A)
- pass_2_date (YYYY-MM-DD)
- contains_virus (Y, N, N/A)
  - Run `System Center Endpoint Protection`
- contains_pii (Y, N, N/A)
  - Run `bulk_extractor.exe`
- made_dip (Y, N, N/A)
  - Run `make_dips.py`
- separation (Y, N)

##
- group_title
- group_num
- [title](https://sites.google.com/a/umich.edu/bhl-archival-curation/processing-archival-collections/09-description/c-aspace-archival-objects#basic)
> The "Title" element will be used to describe intellectual entities (such as a Series or Subseries) as well as actual manifestations of archival materials (Instances or Digital Objects).  As such, it should provide researchers and reference staff with a clear and unambiguous idea of the nature and scope of materials. 

> Avoid jargon or idiosyncratic terms in Title elements and be sure that abbreviations are spelled out. 

> Avoid describing content as "miscellaneous".
- [date_of_content](https://sites.google.com/a/umich.edu/bhl-archival-curation/processing-archival-collections/09-description/c-aspace-archival-objects#dates
) (YYYY, YYYY-YYYY, YYYY-MM-DD, YYYY-MM-DD to YYYY-MM-DD, undated)
- [access_restrictions](https://sites.google.com/a/umich.edu/bhl-archival-curation/processing-archival-collections/09-description/c-aspace-archival-objects#notes
) (open, reading room, restrict ER/PR/SR/CR)
- general_note
> The "General" note is used to provide additional information about the scope or nature of material and is typically applied at the "File" Level of Description.  General notes should help clarify the contents of a folder (or folders) or highlight content that is not readily apparent from the folder titles.
- processing_note

## Post-transfer
- resource_id
- parent_archival_object_link
- parent_archival_object_id
- archival_object_link
- archival_object_id
- digital_object_id
- deepblue_handle
- mivideo_id