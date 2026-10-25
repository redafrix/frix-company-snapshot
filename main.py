import asyncio,json,os
from pathlib import Path
from apify import Actor
from core import inputs,snapshot

async def main():
 async with Actor:
  value=await Actor.get_input() or {'sirens':['552032534']}
  identifiers,previous=inputs(value)
  for index,siren in enumerate(identifiers):
   if index:await asyncio.sleep(1)  # Below the official API's 7 req/s ceiling.
   row=await asyncio.to_thread(snapshot,siren,previous.get(siren))
   if row['billable']:
    result=await Actor.push_data(row,charged_event_name='company-snapshot')
    if result.event_charge_limit_reached:break
   else:await Actor.push_data(row)  # Invalid/missing/unavailable/excluded answers are free.
if __name__=='__main__':asyncio.run(main())
