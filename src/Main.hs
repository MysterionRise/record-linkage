{-# LANGUAGE OverloadedStrings #-}

module Main where

import Network.HTTP.Conduit (simpleHttp)
import qualified Data.ByteString.Lazy.Char8 as Ch
import Text.XML.Cursor (Cursor, attributeIs, content, element, fromDocument, child,
                                ($//), (&|), (&//), (>=>))
import qualified Data.Text as T
import Text.HTML.DOM (parseLBS)

-- the URL we're going to parse
url = "http://www.sports.ru/fantasy/basketball/league/10942.html"

findTeamNodes :: Cursor -> [Cursor]
findTeamNodes = element "table" >=> attributeIs "class" "profile-table" >=> child

extractData = T.concat . content

processData =  putStrLn . T.unpack . T.concat

cursorFor :: String -> IO Cursor
cursorFor u = do
     page <- simpleHttp u
     return $ fromDocument $ parseLBS page

main :: IO ()
main = do
    putStrLn url
    cursor <- cursorFor url
    processData $ cursor $// findNodes &| extractData


